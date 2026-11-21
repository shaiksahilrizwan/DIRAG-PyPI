from pathlib import Path

import typer

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ollama import ResponseError
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ChatHandler.chat import Chat
from Config.configLoader import ConfigLoader
from Config.directoryLoaderPDF import DirectoryLoaderPDF
from Config.models import QueryClassifier
from Config.textSpliter import RecursiveTextSplitter
from Config.vectorStoreHandler import VectorStoreHandler
from Exceptions.exceptions import InvalidConfigJson, InvalidDictKeys

app = typer.Typer(help="DIRAG local Ollama and PDF RAG CLI", no_args_is_help=True)


@app.command()
def chat(session: str | None = typer.Option(None, "--session", "-s")) -> None:
    """Start or resume an interactive chat."""
    console = Console()

    try:
        loader = ConfigLoader()
        if not loader.config:
            raise InvalidConfigJson("Malformed configuration JSON")
        config = loader.get_config()

        llm = ChatOllama(base_url=config["ollama_url"], model=config["model"])

        if session:
            chat_context = Chat()
            chat_context.load_session(session)
            for message in chat_context.writable_chat_hist:
                if "human" in message:
                    console.print(f"[bold cyan]You:[/] {message['human']}")
                elif "ai" in message:
                    console.print(Panel(message["ai"], title="AI", border_style="green"))
        else:
            chat_context = Chat(system_prompt="You are a useful AI assistant.")

        parser = StrOutputParser()
        classifier_parser = PydanticOutputParser(pydantic_object=QueryClassifier)
        rag_session = False
        vc = None

        if "embed_model" in config and "collection_name" in config:
            pdf_files = list(Path.cwd().glob("*.pdf"))
            if pdf_files:
                console.print("PDF documents found; initializing RAG...")
                rag_session = True
                store_path = Path.cwd() / "vstore"
                embeddings = OllamaEmbeddings(
                    base_url=config["ollama_url"], model=config["embed_model"]
                )
                vc = VectorStoreHandler(
                    embed_model=embeddings,
                    collection_name=config["collection_name"],
                )
                if not store_path.is_dir() or not any(store_path.iterdir()):
                    loader_pdf = DirectoryLoaderPDF(str(Path.cwd()))
                    docs = loader_pdf.load_all_docs()
                    splitter = RecursiveTextSplitter(100, 25)
                    chunks = splitter.get_chunks(docs)
                    vc.save_docs(chunks)

        while True:
            human_message = Prompt.ask("[bold cyan]You[/]")
            if human_message.lower() in {"exit", "quit"}:
                chat_context.save_new_session()
                break

            chat_context.add_human_message(human_message)

            if rag_session and vc is not None:
                prompt_template = PromptTemplate(
                    template=(
                        "User query: {chat_message}. Decide whether retrieval is needed. "
                        "Return {format_instructions}"
                    ),
                    input_variables=["chat_message"],
                    partial_variables={"format_instructions": classifier_parser.get_format_instructions()},
                )
                result = llm.invoke(prompt_template.invoke({"chat_message": human_message}))
                classification = classifier_parser.parse(result.content)
                if classification.isRAGRequired and classification.query:
                    context_docs = vc.get_docs(classification.query, no_records=2)
                    context = "\n".join(doc.page_content for doc in context_docs)
                    if context:
                        updated_message = (
                            f"{human_message}\nUse this retrieved context only when useful:\n{context}"
                        )
                        chat_context.writable_chat_hist.pop()
                        chat_context.chat_hist.pop()
                        chat_context.add_human_message(updated_message)

            chat_prompt = chat_context.get_chat_prompt()
            ai_message = (chat_prompt | llm | parser).invoke({})
            chat_context.add_ai_message(ai_message)
            console.print(Panel(ai_message, title="AI", border_style="green"))

    except InvalidDictKeys:
        console.print("[red]Invalid JSON keys. Check dirag.json and try again.[/]")
        raise typer.Exit(code=1)
    except FileNotFoundError:
        console.print("[red]No dirag.json found in the current directory.[/]")
        raise typer.Exit(code=1)
    except ResponseError as exc:
        console.print(f"[red]Ollama API error: {exc}[/]")
        raise typer.Exit(code=1)
    except Exception as exc:
        console.print(f"[red]Error occurred: {exc}[/]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

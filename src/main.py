import os
import shutil
import sys

from markdown_to_html import markdown_to_html_node, extract_title


def copy_static_to_docs(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied {source_path} -> {destination_path}")
        else:
            copy_static_to_docs(source_path, destination_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            if source_path.endswith(".md"):
                destination_path = destination_path.replace(".md", ".html")
                generate_page(
                    source_path,
                    template_path,
                    destination_path,
                    basepath,
                )
        else:
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
                basepath,
            )

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_docs("static", "docs")

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
	basepath,
    )


main()

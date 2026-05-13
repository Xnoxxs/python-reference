


import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


class MyTemplate:

    # -------------------------------------------------------------
    # Load & Render HTML Template with Jinja
    # -------------------------------------------------------------
    @classmethod
    def insert_data_to_html(cls, html_file: str, email_data: dict) -> str:
        """
        Load an HTML designs file and render it using Jinja variables.
        """

        # Path to the Designs/ folder
        template_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "Design")
        )

        # Enable file-based designs loading
        # This allows you to import an html file into another
        # Ex: {% include "footer.html" %} into new_user_sign_up.html
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html"])
        )

        # Load main designs
        template = env.get_template(html_file)

        # Render it
        return template.render(**email_data)

    # -------------------------------------------------------------
    # Generate preview.html for browser viewing
    # -------------------------------------------------------------

    @classmethod
    def preview_template(cls, html_file: str, fake_data: dict):
        """
        Takes an HTML designs + test repositories → generates preview.html
        """

        print("Rendering designs...")

        try:
            html = cls.insert_data_to_html(html_file, fake_data)
        except Exception as e:
            print(f"❌ Error while rendering: {e}")
            return

        output_path = os.path.join(os.path.dirname(__file__), "result.html")

        # Save rendered HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        print("\n✅ Preview generated successfully!")
        print(f"📄 File saved at: {output_path}")
        print("🌍 Open preview.html in your browser to view the email.\n")


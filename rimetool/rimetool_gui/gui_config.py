class GUIConfig:
    # Text for the Beian link
    ICP_BEIAN_TEXT = "晋ICP备2025058330号"

    # Website name and title
    WEBSITE_NAME = "你好👋"
    WEBSITE_TITLE = "医键通词库转换工具"

    # Optional: provide the full Google AdSense snippet to render on the page.
    # Leave empty to disable ads by default.
    GOOGLE_AD_SNIPPET = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5988994930330758" crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-5988994930330758"
         data-ad-slot="3211445360"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    """.strip()

    # Optional: custom notice displayed on the homepage. Leave empty to hide the notice.
    CUSTOM_NOTICE_HTML = "这是一条消息"

    # ads.txt lines served at https://<domain>/ads.txt
    ADS_TXT_LINES = "google.com, pub-5988994930330758, DIRECT, f08c47fec0942fa0"

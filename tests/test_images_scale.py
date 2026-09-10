def test_settings_images_scale_default():
    # directly execute the line: images_scale: float = 1.0
    from docling_mcp.settings.conversion import Settings

    s = Settings()
    assert s.images_scale == 1.0


def test_get_converter_applies_images_scale(monkeypatch):
    
    # This test executes pipeline_options.images_scale = settings.images_scale
    # mock out heavy classes so we don't initialize real Docling converter logic
    
    import docling_mcp.tools.conversion as conv

    # clear cache to prevent skipping of test execution
    conv._get_converter.cache_clear()

    # Force settings to a known non-default value
    monkeypatch.setattr(conv.settings, "keep_images", False, raising=False)
    monkeypatch.setattr(conv.settings, "images_scale", 2.5, raising=False)

    created = {}

    class FakePdfPipelineOptions:
        def __init__(self):
            created["options"] = self
            self.generate_page_images = None
            self.images_scale = None

    class FakePdfFormatOption:
        def __init__(self, pipeline_options=None, **kwargs):
            self.pipeline_options = pipeline_options
            self.kwargs = kwargs

    class FakeDocumentConverter:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    # Patch the names used inside docling_mcp.tools.conversion
    monkeypatch.setattr(conv, "PdfPipelineOptions", FakePdfPipelineOptions)
    monkeypatch.setattr(conv, "PdfFormatOption", FakePdfFormatOption)
    monkeypatch.setattr(conv, "DocumentConverter", FakeDocumentConverter)

    # Run the function under test
    converter = conv._get_converter()

    assert "options" in created, "PdfPipelineOptions was not constructed"
    assert created["options"].generate_page_images is False
    assert created["options"].images_scale == 2.5

    # ensure converter creation happened
    assert isinstance(converter, FakeDocumentConverter)

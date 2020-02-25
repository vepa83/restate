# this file required to work with thumbnails


class CustomStrategy(object):
    def on_existence_required(self, file):
        file.generate()

    def on_content_required(self, file):
        file.generate()

    def on_source_saved(self, file):
        file.generate()

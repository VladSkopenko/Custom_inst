from fastapi.staticfiles import StaticFiles


class StaticFilesCache(StaticFiles):
    def __init__(
        self,
        *args,
        cachecontrol="public, max-age=31536000, s-maxage=31536000, immutable",
        **kwargs,
    ):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp

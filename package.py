from Jumpscale import j

class Package(j.baseclasses.threebot_package):
    """
    kosmos -p
    cl = j.servers.threebot.local_start_default()
    j.threebot.packages.zerobot.packagemanager.actors.package_manager.package_add(git_url="https://github.com/Pishoy/www_enertia_io")
    """

    def _init(self, **kwargs):
        self.branch = kwargs["package"].branch or "master"
        self.enertia_io = "https://github.com/Pishoy/www_enertia_io"

    def prepare(self):
        for port in (443, 80):
            website = self.openresty.get_from_port(port)
            locations = website.locations.get("enertia")
            static_location = locations.locations_static.new()
            static_location.name = "enertia_static"
            static_location.path_url = "/enertia"
            path = j.clients.git.getContentPathFromURLorPath(self.enertia_io, branch=self.branch, pull=True)
            html_path = "{0}/html".format(path)
            static_location.path_location = html_path
            static_location.use_jumpscale_weblibs = True # if set, will copy weblibs and serve it from /static/weblibs directly
            locations.configure()
            website.configure()

    def start(self):
        self.prepare()

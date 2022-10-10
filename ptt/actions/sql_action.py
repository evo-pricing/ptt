from ptt import settings


class SQLAction:
    def __init__(self, dsn) -> None:
        self.dsn = dsn

    def get_ds(self):
        ds_name = settings.get(
            "servers.default") if self.dsn == None else self.dsn
        ds_list = settings.get("servers.dataSources")

        for ds in ds_list:
            if ds['name'] == ds_name:
                return ds['connectionString']

        raise Exception('No connection string found, check configuration')

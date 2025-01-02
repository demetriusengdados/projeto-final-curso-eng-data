dbutils.fs.mount(
    source="abfss://<seu-container-name>@<seu-adls-account-name>.dfs.core.windows.net/",
    mount_point="/mnt/adls",
    extra_configs={"fs.azure.account.key.<seu-adls-account-name>.dfs.core.windows.net": "<seu-sas-token>"}
)

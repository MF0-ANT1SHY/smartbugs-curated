import solcx
versions = solcx.get_installable_solc_versions()

for version in versions:
    try:
        print(f"Installing solc {version}...")
        solcx.install_solc(version)
        print(f"Successfully installed {version}")
    except Exception as e:
        print(f"Failed to install {version}: {e}")

# 显示已安装的版本
installed = solcx.get_installed_solc_versions()
print(f"\nTotal installed versions: {len(installed)}")
print(installed)
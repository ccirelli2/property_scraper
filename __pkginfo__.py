numversion = (2, 0, 1)
dev_version = '4'

version = '.'.join(str(num) for num in numversion)
if dev_version is not None:
    version += '-dev' + str(dev_version)

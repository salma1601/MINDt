DISTNAME = 'mindt'
DESCRIPTION = 'MRI Rodents processing in Python'
with open('README.rst') as fp:
    LONG_DESCRIPTION = fp.read()
MAINTAINER = 'Nachiket Nadkarni'
MAINTAINER_EMAIL = 'nadkarni@fastmail.fm'
URL = 'https://github.com/samll-animal-MRI/MINDt'
LICENSE = 'CeCILL-B'
DOWNLOAD_URL = 'https://github.com/samll-animal-MRI/MINDt'


if __name__ == "__main__":
    if is_installing():
        module_check_fn = _VERSION_GLOBALS['_check_module_dependencies']
        module_check_fn(is_mindt_installing=True)

    install_requires = \
        ['%s>=%s' % (mod, meta['min_version'])
            for mod, meta in _VERSION_GLOBALS['REQUIRED_MODULE_METADATA']
            if not meta['required_at_installation']]

    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS',
              'Programming Language :: Python :: 2.7',
          ],
          packages=find_packages(),
          package_data={'mindt.data_fetchers.description': ['*.rst']},
          install_requires=install_requires,)

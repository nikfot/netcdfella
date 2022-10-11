<a name="readme-top"></a>

[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nikfot/netcdfella">
    <img src="https://github.com/nikfot/netcdfella/blob/master/assets/netcdfella_logo.png" alt="Logo" height="300" width="auto">
  </a>

  <h3 align="center">NetcdFella</h3>

  <p align="center">
    The easy as duck duck netcdf converter to ASCII, JPEG and more...
    <br />
    <a href="https://github.com/nikfot/netcdfella"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/nikfot/netcdfella/issues">Report Bug</a>
    ·
    <a href="https://github.com/nikfot/netcdfella/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Netcdfella is a command line interface (cli) tool for converting netcdf files to ASCII and JPG/PNG format, as well as creating graphs based on the vectors of the file.

Netcdfella supports two ways for converting documents at the time being:

- single/multi convert
- conversion upon creation

During the run of the cli the output types, the mapping dimension and variable can be selected aling with other options.

### single/multi convert

You can convert a single file or all netcdf files in a directory on your command. This is the case of the single/multi select.

### conversion upon creation

A directory can be selected to be watched by netcdfella. WHen a new netcdf file is created in that directory, it is automatically converted in the selected formats.

#### qnotify

In order to handle any amount of input documents in the case of watch. A producer-consumer queue is created in the module qnotify using the inotify library. In this case the producers are the directory events. This creates a buffer that can handle the set amount of concurrent document creations.

Use the `README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

- [![Python][python]][python-url]
- [![Poetry][poetry]][poetry-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This software and tested for Python version 3.10.4.

If you need to manually install packages:
- Cartopy libgeos
  ```sh
  apt get install libgeos-dev
  ```
  
- requirements
  ```sh
  pip install -r requirements.txt
  ```

If you wish to make use of the pyproject.toml you need to install poetry:

- poetry
  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### Installation

_You can install from source or from pypi_

#### PYPI

Use PYPI to pip install the project:

    ```sh
    pip install netcdfella

#### Source

1. Clone the repo
   ```sh
   git clone https://github.com/nikfot/netcdfella.git
   ```
2. Install using poetry
   ```sh
   poetry install
   ```
3. Run `netcdfella` to see the help with available choices:

   ```sh
   netcdfella
   ```

   or

   ```sh
   netcdfella --help
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

You can use the netcdfella to get a better description of the available choices:

    ```sh
    netcdfella
    ```

    or

    ```sh
    netcdfella --help
    ```

### convert

Use netcdfella to convert a single document or all documents in a directory:

    ```sh
    netcdfella convert "/path/to/documents" -k "ascii,graph,scatter,marks" -md "flashes" -mv "radiance"
    ```

All choices for convert subcommand:
Options:
-o, --output-dir TEXT set the output directory for converted files.
-k, --output-kinds TEXT set the output kind for conversion.
-md, --map-dimension TEXT set the dimenion to use for mapping.
-mv, --map-variable TEXT set the variable to use for mapping.
-e, --exclude-variables TEXT comma separated list of variables to be
excluded from conversion.
--help Show this message and exit.

### watch

Use netcdfella to watch over a directory and convert files upon creation:

    ```sh
    netcdfella watch "/path/to/documents" -k "ascii,graph,scatter,marks" -md "flashes" -mv "radiance"
    ```

Options:
-o, --output-dir TEXT set the output directory for converted files.
-k, --output-kinds TEXT set the output kind for conversion.
-md, --map-dimension TEXT set the dimenion to use for mapping.
-mv, --map-variable TEXT set the variable to use for mapping.
-e, --exclude-variables TEXT comma separated list of variables to be
excluded from conversion.
--help Show this message and exit.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Add cli conversion
- [x] Add ascii,jpg/png, graphs
- [ ] Add docker support
- [ ] Check compatibility with more netcdf filetypes (current test METEOSAT 4th gen)
- [ ] Add REST API Server
- [ ] Add gui

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

There are still a lot to be done, so if you find the project usefull please contribute you comments, ideas and code. It is **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the GPL License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Nikos Fotiou - [@workaround18](https://twitter.com/workaround18) - nik_fot@hotmail.gr

Netcdfella: [https://github.com/nikfot/netcdfella](https://github.com/nikfot/netcdfella)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

This tool is created as part of my postgrad studies "Space Technologies Applications and Services - STAR" programm at the National and Kapodestrian University of Athens Greece (NKUA). It was a semester project for the class "Space Image Processing" by professor Stavros Kolios.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[issues-shield]: https://img.shields.io/badge/github-issues-gray?style=for-the-badge&logo=Github
[issues-url]: https://github.com/nikfot/netcdfella/issues
[license-shield]: https://img.shields.io/pypi/l/netcdfella?style=plastic
[license-url]: https://github.com/nikfot/netcdfella/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/nikosfotiou/
[netcdfella-logo]: assets/netcdfella_logo.png
[python]: https://img.shields.io/badge/python-yellow?style=for-the-badge&logo=Python
[python-url]: https://www.python.org/
[poetry]: https://img.shields.io/badge/poetry-blue?style=for-the-badge&logo=Poetry
[poetry-url]: https://python-poetry.org/

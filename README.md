![PyPI - Version](https://img.shields.io/pypi/v/droneframe)
![GitHub release (with filter)](https://img.shields.io/github/v/release/anwaraliahmad/droneframe)
![GitHub](https://img.shields.io/github/license/anwaraliahmad/droneframe)
# Droneframe
A simple CLI tool to extract frames from drone footages with EXIF data included.

## Installation
You can install DroneFrame from either from PyPI using `pip` or directly through GitHub releases.
### Pip
```bash
$ pip install droneframe
```
### GitHub 
#### Install From Source
```bash
$ git clone https://github.com/anwaraliahmad/droneframe.git
$ cd droneframe 
$ pip install
```
#### Install From Release
1. Navigate to [releases page](https://github.com/anwaraliahmad/droneframe/releases)
2. Download either `.tar.gz` or `.whl`
3. Navigate to your download
```bash
$ pip install droneframe-version.<tar.gz or whl>
```
## Running
#### Arguments
| Argument/Option 	| Description                                              	| Flags                	| Default                                        	| Required                        	|
|-----------------	|----------------------------------------------------------	|----------------------	|------------------------------------------------	|---------------------------------	|
| **video**       	| Path to drone video file (`.MP4`)                        	|                      	|                                                	| **Yes**                         	|
| `meta`          	| Path to metadata file (`.SRT`)                           	| `-m`, `--meta`       	| Same pathname (sans file extension) as `video` 	| No                              	|
| `frame_rate`    	| The rate for frame extraction                            	| `-f`, `--frame_rate` 	| 30                                             	| No (but **highly** recommended) 	|
| `output`        	| Path to output folder  	| `-o`, `--output`     	| Generates `./frames` (in working directory)              	| No                              	|
| Help            	| Display help message                                     	| `-h`, `--help`       	|                                                	|                                 	|
## Example: Photogrammetry

### Process
1. Use `droneframe` to get frames filled with GPS & timestamp data.
```bash
$ droneframe path/to/DJI_001.MP4 -f 3 # Large drone video of subject.
```
2. Import the `./frames` folder into your photogrammetry software of choice.
3. Enjoy your 3D recreation.
> If constraints permit, you can always extract more with a higher framerate or generate an additional batch of frames from another video you have of the target.

### End Result
![Abandoned Railyard Flue](https://i.imgur.com/wQro7HK.png)

This is a model of an abandoned structure that was created by running `droneframe` and uploading the resulting frames onto [WebODM Lightning](https://webodm.net/) for 3D reconstruction.

_You can interact with the full model on [Sketchfab](https://sketchfab.com/3d-models/abandoned-railyard-flue-3c92d642af34444dadc83f1d2d0dd07d)_


## License
This project is licensed under the MIT License. See the LICENSE file for details.




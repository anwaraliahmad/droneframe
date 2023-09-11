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
| `output`        	| Target path to output folder (will generate a folder named after the video file there) 	| `-o`, `--output`     	|  Working directory              	| No                              	|
| Help            	| Display help message                                     	| `-h`, `--help`       	|                                                	|                                 	|
## Example: Photogrammetry

### Process
1. Use `droneframe` to get frames filled with GPS & timestamp data.
```bash
$ droneframe path/to/DJI_001.MP4 -f 3 # Large drone video of subject.
```
2. Import the generated `./DJI_001` folder into your photogrammetry software of choice.
3. Enjoy your 3D recreation.
> If constraints permit, you can always extract more with a higher framerate or generate an additional batch of frames from another video you have of the target.

### End Result
<center> <div class="sketchfab-embed-wrapper"> <iframe title="Abandoned Railyard Flue" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/3c92d642af34444dadc83f1d2d0dd07d/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/abandoned-railyard-flue-3c92d642af34444dadc83f1d2d0dd07d?utm_medium=embed&utm_campaign=share-popup&utm_content=3c92d642af34444dadc83f1d2d0dd07d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Abandoned Railyard Flue </a> by <a href="https://sketchfab.com/anwaraliahmad?utm_medium=embed&utm_campaign=share-popup&utm_content=3c92d642af34444dadc83f1d2d0dd07d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> anwaraliahmad </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=3c92d642af34444dadc83f1d2d0dd07d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p></div>
</center>

This is a model of an abandoned structure that was created by running `droneframe` and uploading the resulting frames onto [WebODM Lightning](https://webodm.net/) for 3D reconstruction.


## License
This project is licensed under the MIT License. See the LICENSE file for details.




install-deps:
						@echo "Installing dependanies" 
						brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
						brew install pyenv
						brew install python3
						pyenv install 3.6.2
						pip3 install Cython==0.26.1


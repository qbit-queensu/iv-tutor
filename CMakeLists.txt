cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(IV_Tutor)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/IV_Tutor")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "Andrew Kim (Queen's University)")
set(EXTENSION_DESCRIPTION "IV Tutor Extension")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/IV_Tutor.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/IV_Tutor/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(IVTutor)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})

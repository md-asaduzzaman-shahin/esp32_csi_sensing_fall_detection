# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "C:/Espressif/frameworks/esp-idf-v5.5.2/components/bootloader/subproject")
  file(MAKE_DIRECTORY "C:/Espressif/frameworks/esp-idf-v5.5.2/components/bootloader/subproject")
endif()
file(MAKE_DIRECTORY
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader"
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix"
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/tmp"
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/src"
  "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/Shahin/WorkThings/WorksNPractices/projects/wifi_sensing_csi/XIAO_esp-csi-master2/examples/room_presence_detection/send_TX/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()

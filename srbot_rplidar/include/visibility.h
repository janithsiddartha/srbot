// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef VISIBILITY_H_
#define VISIBILITY_H_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__

  #ifdef __GNUC__
    #define srbot_rplidar_EXPORT __attribute__ ((dllexport))
    #define srbot_rplidar_IMPORT __attribute__ ((dllimport))
  #else
    #define srbot_rplidar_EXPORT __declspec(dllexport)
    #define srbot_rplidar_IMPORT __declspec(dllimport)
  #endif

  #ifdef srbot_rplidar_DLL
    #define srbot_rplidar_PUBLIC srbot_rplidar_EXPORT
  #else
    #define srbot_rplidar_PUBLIC srbot_rplidar_IMPORT
  #endif

  #define srbot_rplidar_PUBLIC_TYPE srbot_rplidar_PUBLIC

  #define srbot_rplidar_LOCAL

#else

  #define srbot_rplidar_EXPORT __attribute__ ((visibility("default")))
  #define srbot_rplidar_IMPORT

  #if __GNUC__ >= 4
    #define srbot_rplidar_PUBLIC __attribute__ ((visibility("default")))
    #define srbot_rplidar_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define srbot_rplidar_PUBLIC
    #define srbot_rplidar_LOCAL
  #endif

  #define srbot_rplidar_PUBLIC_TYPE
#endif

#ifdef __cplusplus
}
#endif

#endif  // VISIBILITY_H_

cmake_minimum_required(VERSION 3.16.0)
project(Analyzer_v2 VERSION 2.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Linux 平台配置
if(UNIX AND NOT APPLE)
    message(STATUS "配置为 Linux 平台 (在 Analyzer_v2 子目录)")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")
    
    # 编译模式
    if(NOT CMAKE_BUILD_TYPE)
        set(CMAKE_BUILD_TYPE Release)
    endif()
    
    set(CMAKE_CXX_FLAGS_DEBUG "-O0 -Wall -g")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall")
    
    # 查找 OpenCV
    find_package(OpenCV REQUIRED)
    if(OpenCV_FOUND)
        message(STATUS "找到 OpenCV: ${OpenCV_VERSION}")
        include_directories(${OpenCV_INCLUDE_DIRS})
    else()
        message(FATAL_ERROR "未找到 OpenCV，请安装: sudo apt install libopencv-dev")
    endif()
    
    # 使用 pkg-config 查找库
    find_package(PkgConfig REQUIRED)
    
    # FFmpeg 库
    pkg_check_modules(LIBAV REQUIRED 
        libavformat 
        libavcodec 
        libavutil 
        libswscale 
        libswresample
        libavdevice
    )
    
    # 其他库
    pkg_check_modules(CURL REQUIRED libcurl)
    pkg_check_modules(EVENT REQUIRED libevent)
    pkg_check_modules(JSONCPP REQUIRED jsoncpp)
    
    # turbojpeg (可选)
    pkg_check_modules(TURBOJPEG libturbojpeg)
    
    # 头文件路径
    include_directories(
        ${OpenCV_INCLUDE_DIRS}
        ${LIBAV_INCLUDE_DIRS}
        ${CURL_INCLUDE_DIRS}
        ${EVENT_INCLUDE_DIRS}
        ${JSONCPP_INCLUDE_DIRS}
    )
    
    if(TURBOJPEG_FOUND)
        include_directories(${TURBOJPEG_INCLUDE_DIRS})
    endif()
    
    # 源文件
    set(source
        Core/Analyzer.cpp
        Core/AvPullStream.cpp
        Core/AvPushStream.cpp
        Core/Config.cpp
        Core/ControlExecutor.cpp
        Core/GenerateAlarm.cpp
        Core/GenerateVideo.cpp
        Core/Scheduler.cpp
        Core/Server.cpp
        Core/Utils/Request.cpp
        main.cpp
    )
    
    # 创建可执行文件
    add_executable(Analyzer_v2 ${source})
    
    # 链接库
    target_link_libraries(Analyzer_v2 
        ${OpenCV_LIBS}
        ${LIBAV_LIBRARIES}
        ${CURL_LIBRARIES}
        ${EVENT_LIBRARIES}
        ${JSONCPP_LIBRARIES}
        pthread
        rt  # 用于 clock_gettime
    )
    
    if(TURBOJPEG_FOUND)
        target_link_libraries(Analyzer_v2 ${TURBOJPEG_LIBRARIES})
    endif()
    
    # 复制配置文件
    add_custom_command(TARGET Analyzer_v2 POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CMAKE_SOURCE_DIR}/config.json"
        "$<TARGET_FILE_DIR:Analyzer_v2>/config.json"
    )
    
    message(STATUS "================================")
    message(STATUS "  Analyzer_v2 构建配置")
    message(STATUS "================================")
    message(STATUS "构建类型: ${CMAKE_BUILD_TYPE}")
    message(STATUS "OpenCV版本: ${OpenCV_VERSION}")
    message(STATUS "================================")
    
else()
    message(WARNING "此 CMakeLists.txt 仅支持 Linux 平台")
    message(WARNING "请使用项目根目录的 CMakeLists.txt 进行 Windows 构建")
endif()






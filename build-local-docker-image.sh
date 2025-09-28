#!/bin/bash
# script to build local docker image.
# highlevel steps involved
# 1. Stop and remove existing container and image
# 2. Install dependencies
# 3. Build nc-gui
#   3a. static build of nc-gui
#   3b. copy nc-gui build to nocodb dir
# 4. Build nocodb

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LOG_FILE=${SCRIPT_DIR}/build-local-docker-image.log
ERROR=""

function stop_and_remove_container() {
    # Stop and remove the existing container
    docker stop nocodb-local >/dev/null 2>&1
    docker rm nocodb-local >/dev/null 2>&1
}

function remove_image() {
    # Remove the existing image
    docker rmi nocodb-local >/dev/null 2>&1
}

function install_dependencies() {
    # Install all dependencies
    cd ${SCRIPT_DIR}
    pnpm bootstrap || ERROR="install_dependencies failed"
}

function build_gui() {
    # build nc-gui
    export NODE_OPTIONS="--max_old_space_size=16384"
    # generate static build of nc-gui
    cd ${SCRIPT_DIR}/packages/nc-gui
    pnpm run generate || ERROR="gui build failed"
}

function copy_gui_artifacts() {
     # copy nc-gui build to nocodb dir
    rsync -rvzh --delete ./dist/ ${SCRIPT_DIR}/packages/nocodb/docker/nc-gui/ || ERROR="copy_gui_artifacts failed"
}

function package_nocodb() {
    # build nocodb ( pack nocodb-sdk and nc-gui )
    cd ${SCRIPT_DIR}/packages/nocodb
    pnpm run docker:build || ERROR="package_nocodb failed"
}

function build_image() {
    # build docker
    echo "Current directory: $(pwd)"
    echo "Looking for Dockerfile.local..."
    ls -la Dockerfile.local || echo "Dockerfile.local not found in current directory"
    
    # Ensure we're in the nocodb package directory for the build
    cd ${SCRIPT_DIR}/packages/nocodb
    echo "Building from directory: $(pwd)"
    echo "Available files:"
    ls -la | head -10
    
    docker build . -f Dockerfile.local -t nocodb-local || ERROR="build_image failed"
}

function log_message() {
    if [[ ${ERROR} != "" ]];
    then
        >&2 echo "build failed, Please check build-local-docker-image.log for more details"
        >&2 echo "ERROR: ${ERROR}"
        
        # Show the last 50 lines of the log for debugging
        echo "=== Last 50 lines of build log ==="
        tail -50 ${LOG_FILE} 2>/dev/null || echo "Could not read log file"
        echo "================================="
        
        exit 1
    else
        echo 'docker image with tag "nocodb-local" built sussessfully. Use below sample command to run the container'
        echo 'docker run -d -p 3333:8080 --name nocodb-local nocodb-local '
        
        # Verify the image was actually created
        if docker images | grep -q nocodb-local; then
            echo "✅ Verified: nocodb-local image exists"
        else
            >&2 echo "❌ ERROR: nocodb-local image was not created despite no build errors!"
            exit 1
        fi
    fi
}

echo "Info: Stopping and removing existing container and image" | tee ${LOG_FILE}
stop_and_remove_container
remove_image

echo "Info: Installing dependencies" | tee -a ${LOG_FILE}
install_dependencies 1>> ${LOG_FILE} 2>> ${LOG_FILE}

echo "Info: Building nc-gui" | tee -a ${LOG_FILE}
build_gui 1>> ${LOG_FILE} 2>> ${LOG_FILE}

echo "Info: Copy nc-gui build to nocodb dir" | tee -a ${LOG_FILE}
copy_gui_artifacts 1>> ${LOG_FILE} 2>> ${LOG_FILE}

echo "Info: Build nocodb, package nocodb-sdk and nc-gui" | tee -a ${LOG_FILE}
package_nocodb 1>> ${LOG_FILE} 2>> ${LOG_FILE}

if [[ ${ERROR} == "" ]]; then
    echo "Info: Building docker image" | tee -a ${LOG_FILE}
    build_image 1>> ${LOG_FILE} 2>> ${LOG_FILE}
fi

log_message | tee -a ${LOG_FILE}

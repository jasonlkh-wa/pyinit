#!/bin/zsh

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
    -n | --name)
        script_name="$2"
        shift
        shift
        ;;
    -f | --folder)
        folder_path="$2"
        shift
        shift
        ;;
    -venv | --conda-env)
        conda_env="$2"
        shift
        shift
        ;;
    *)
        echo "Invalid option: $1" >&2
        exit 1
        ;;
    esac
done

# Create directories and files
mkdir -p "${folder_path}/test" "${folder_path}/resources"
cd "${folder_path}"
touch $script_name
echo 'if __name__ == "__main__":\n\tpass' >>$script_name
mkdir -p .vscode/
touch .vscode/settings.json
echo '{"python.defaultInterpreterPath":"'${HOME}/opt/miniconda3/envs/${conda_env}'/bin/python"}' >.vscode/settings.json

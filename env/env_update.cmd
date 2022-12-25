@echo off
call env_config
call conda env update -n %PROJECT_ENV% -f environment.yml

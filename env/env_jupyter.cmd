@echo off
call env_config
call activate %PROJECT_ENV%
call cd %MAIN_DIR%
call jupyter notebook
cmd

import os
import sys
import importlib


def import_py_files(package_dir, package_name):
    # package_dir을 sys.path에 추가하여 import 경로에 포함시킵니다.
    sys.path.insert(0, package_dir)

    # __main__을 처리할 경우의 경로 조정
    if package_name == "__main__":
        package_name = os.path.basename(package_dir)  # 디렉토리 이름으로 변경

    for root, _, files in os.walk(package_dir):
        # '_'로 시작하는 디렉토리는 무시
        if os.path.basename(root).startswith("_"):
            continue

        for file in files:
            # __init__.py를 제외한 .py 파일을 import
            if file.endswith(".py") and file != "__init__.py":
                # 상대 경로를 패키지 경로에 맞게 변환
                module_path = os.path.relpath(
                    os.path.join(root, file), package_dir
                ).replace(os.sep, ".")[:-3]

                # 모듈 임포트
                try:
                    importlib.import_module(f"{package_name}.{module_path}")
                except ModuleNotFoundError as e:
                    print(f"Module not found: {package_name}.{module_path}")
                    raise e


# 현재 디렉토리와 패키지 이름으로 모든 .py 파일을 import
import_py_files(os.path.dirname(__file__), __name__)

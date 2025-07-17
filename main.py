import subprocess
import sys
import os
from pathlib import Path


def run_font_subsetting():
    """폰트 서브셋팅을 실행합니다."""
    
    # 입력 파일들 확인
    input_font = "PretendardVariable.woff2"
    glyphs_file = "glyphs.txt"
    output_dir = "./subset-fonts-output"
    output_font = f"{output_dir}/PretendardVariable.woff2"
    
    # 입력 파일 존재 확인
    if not os.path.exists(input_font):
        print(f"❌ 오류: 입력 폰트 파일 '{input_font}'을 찾을 수 없습니다.")
        return False
    
    if not os.path.exists(glyphs_file):
        print(f"❌ 오류: 문자 목록 파일 '{glyphs_file}'을 찾을 수 없습니다.")
        return False
    
    # 출력 디렉토리 생성
    Path(output_dir).mkdir(exist_ok=True)
    
    # pyftsubset 명령어 구성 https://www.44bits.io/ko/post/optimization_webfont_with_pyftsubnet#%ED%8F%B0%ED%8A%B8-%EC%B5%9C%EC%A0%81%ED%99%94%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%98%B5%EC%85%98
    cmd = [
        "pyftsubset",                    
        input_font,                       
        "--flavor=woff2",                 
        f"--output-file={output_font}",   
        f"--text-file={glyphs_file}",     
        "--layout-features=*",
        "--glyph-names",                  
        "--symbol-cmap",                  
        "--legacy-cmap",                  
        "--notdef-glyph",                 
        "--notdef-outline",               
        "--recommended-glyphs",           
        "--name-legacy",                  
        "--drop-tables=",                 
        "--name-IDs=*",                   
        "--name-languages=*"              
    ]
    
    try:
        print("🚀 폰트 서브셋팅을 시작합니다...")
        print(f"📁 입력 폰트: {input_font}")
        print(f"📄 문자 목록: {glyphs_file}")
        print(f"📁 출력 위치: {output_font}")
        print()
        
        # 명령어 실행
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("✅ 폰트 서브셋팅이 성공적으로 완료되었습니다!")
        print(f"📊 출력 파일: {output_font}")
        
        # 파일 크기 비교
        if os.path.exists(output_font):
            input_size = os.path.getsize(input_font) / (1024 * 1024)  # MB
            output_size = os.path.getsize(output_font) / 1024  # KB
            compression_ratio = (1 - output_size / (input_size * 1024)) * 100
            
            print(f"📈 압축 결과:")
            print(f"   원본 크기: {input_size:.1f} MB")
            print(f"   압축 크기: {output_size:.1f} KB")
            print(f"   압축률: {compression_ratio:.1f}%")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류: 폰트 서브셋팅 중 오류가 발생했습니다.")
        print(f"오류 코드: {e.returncode}")
        if e.stdout:
            print(f"출력: {e.stdout}")
        if e.stderr:
            print(f"오류: {e.stderr}")
        return False
        
    except FileNotFoundError:
        print("❌ 오류: 'pyftsubset' 명령어를 찾을 수 없습니다.")
        print("💡 해결 방법:")
        print("   1. fonttools가 설치되어 있는지 확인하세요: pip install fonttools")
        print("   2. 가상환경이 활성화되어 있는지 확인하세요")
        return False


def main():
    """메인 함수"""
    print("🎨 Font Subsetter")
    print("=" * 50)
    
    success = run_font_subsetting()
    
    if success:
        print("\n🎉 모든 작업이 완료되었습니다!")
    else:
        print("\n💥 작업이 실패했습니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()

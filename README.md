# Monolith
모노리스는 대학생 자작자동차대회 출전 차량을 위한 오픈소스 데이터로깅 플랫폼입니다.

설계도 및 소스코드 일체가 공개되어 있어 누구나 쉽게 직접 제작하여 사용할 수 있습니다.

<br>

모노리스 프로젝트는 다음의 세 가지 요소로 이루어져 있습니다.
* TMA-1 데이터로거 하드웨어(회로도, PCB 설계도, BOM) 및 소프트웨어, 설정 도구
* TMA-2 무선 통신 실시간 중계 서버
* TMA-3 로그 해석 및 데이터 시각화 도구

<br>

모노리스 데이터로거 `TMA-1`은 차량에 장착되어 CAN 트래픽, 가속도, GPS, 아날로그 신호 등 다양한 정보를 수집하고 SD카드에 저장합니다.

저장된 로그는 함께 제공되는 웹 기반의 로그 해석 및 데이터 시각화 도구 `TMA-3`을 통하여 손쉽게 분석할 수 있습니다.

또한, TMA-1은 드라이버가 휴대한 스마트폰의 Wi-Fi 핫스팟에 연결하여 수집한 데이터를 서버에 실시간으로 전송하는 기능을 포함하고 있습니다.

`TMA-2` 중계 서버는 TMA-1로부터 수신한 차량의 주행 데이터를 웹 클라이언트에 실시간으로 중계합니다.

<br>

모노리스에서는 필요한 기능만 골라 HW/SW를 구성할 수 있습니다.

예를 들어, 실시간 데이터 전송 기능을 사용하지 않을 경우 TMA-1 제작 시 ESP32를 장착할 필요가 없습니다. 또한, TMA-2 텔레메트리 서버를 설치하는 절차를 생략해도 됩니다.


<br>

2023 KSAE 대학생 자작자동차대회 기술아이디어 금상 수상작입니다.

<img src='https://github.com/luftaquila/monolith/assets/17094868/53384153-dbec-466c-b6d7-5401e73fa48c' style='width: 400px'>

## TMA-1 데이터로거
차량에 장착되어 데이터를 수집하는 장비입니다. 다음 기능들을 지원합니다.

* 1채널 CAN 버스 트래픽 모니터링
* 8채널 디지털 신호 모니터링
* 4채널 아날로그 신호 모니터링
* 4채널 펄스 신호 모니터링
* 3축 가속도 변화 모니터링
* 외부 GPS 모듈을 통한 위치 정보 모니터링
* RTC 시간 정보 유지 및 관리
* 6개의 상태 표시 LED
* SD카드에 로그 저장
* Wi-Fi로 로그 실시간 전송

또한 함께 제공되는 설정 도구는 다음과 같은 기능을 제공합니다.

* TMA-1 기능 선택적 활성화
* 장비의 RTC에 현재 시간 업데이트
* 중계 서버 주소 설정
* 연결할 핫스팟 네트워크 설정
* 실행 파일 빌드 및 TMA-1 업데이트

### 하드웨어 설계도
TMA-1의 KiCAD 회로 및 PCB 설계도입니다.

### BOM(Bill of Materials)
공개된 PCB 설계도로 TMA-1을 직접 제작하는데 필요한 부품의 목록입니다.

### 임베디드 소프트웨어
TMA-1의 STM32F4 MCU에 업로드하는 STM32CubeIDE/MX 프로젝트와 ESP32에 업로드하는 아두이노 소스코드입니다.

## TMA-2 무선 통신 중계 서버
TMA-1이 Wi-Fi를 통해 전송한 로그를 웹 클라이언트에 실시간으로 중계하는 서버입니다. 

Node.js로 작성되었으며, 소켓 통신을 사용하여 데이터를 주고받습니다.

TMA-2 서버는 직접 self-hosting하여 사용할 수 있습니다. 웹 클라이언트는 각 사용자가 직접 제작해야 합니다.

구현 예시:

<img src='https://github.com/luftaquila/monolith/assets/17094868/5ba95b27-f435-4d70-a965-757269b4843e'><br>

## TMA-3 로그 해석기 및 데이터 분석 도구
모노리스 데이터로거 TMA-1이 SD 카드에 저장하는 로그는 용량 최적화를 위해 바이너리 형식으로 저장되어 있습니다.

저장된 로그를 사람이 읽을 수 있도록 해석하여 json 또는 csv 파일로 변환하는 해석기를 제공합니다.

또한, 로그 해석기와 연동되는 데이터 분석 도구를 통해 해석한 로그를 바로 그래프로 시각화할 수 있습니다. 

TMA-3 로그 해석기와 데이터 분석 도구는 모두 웹 어플리케이션으로 구현되어 브라우저만 있으면 손쉽게 사용할 수 있습니다.

<img src='https://github.com/luftaquila/monolith/assets/17094868/12c3801c-3507-4647-bfbc-e4012fde11ea'>

## 기타
프로젝트의 이름인 모노리스는 아서 C. 클라크의 소설 2001: A Space Odyssey에서 차용하였습니다.

데이터로거와 중계 서버가 달에서 발굴되어 전파를 송신하는 TMA-1과, 이를 수신해 스타게이트를 여는 토성의 TMA-2 모노리스의 역할과 유사하다는 점에 착안했습니다.

## LICENSE
```
"THE BEERWARE LICENSE" (Revision 42):
LUFT-AQUILA wrote this project. As long as you retain this notice,
you can do whatever you want with this stuff. If we meet someday,
and you think this stuff is worth it, you can buy me a beer in return.
```
이 프로젝트의 내용물은 얼마든지 자유롭게 사용할 수 있습니다.

이 프로젝트가 마음에 든다면, 언젠가 우리가 만나게 되었을 때 맥주 한 잔 사 주세요.

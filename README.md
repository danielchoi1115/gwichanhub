# 귀찬헙 (GwichanHub)

GwichanHub은 귀찮은 일인 `Pull Request (PR)` 의 `Merge` 과정을 자동화해주는 서비스입니다.

매일 아침 9시에 https://github.com/it-e-7/Algorithm Repository에 제출된 `PR`들을 검사하고 규칙에 맞게 잘 작성되었을 경우 Main 브랜치에 `Merge`합니다.

검사한 결과는 제출 건수, 반려 사유등과 함께 디스코드 봇을 통해 전송됩니다.

<img src="https://user-images.githubusercontent.com/100273844/235680764-c32cbb95-3850-4418-b0ab-aa89b28bab5e.png" width="600"/>

# 전체 흐름 (Workflow)

![스크린샷 2023-05-01 163135](https://user-images.githubusercontent.com/100273844/235423262-a67fbe73-3913-4733-8fe1-650264c8e670.png)

# Pull 요청 검증 핵심 로직

## 현재 검사중인 항목

검사하는 항목은 [https://github.com/it-e-7/Algorithm#readme](https://github.com/it-e-7/Algorithm#readme)을 기준으로 합니다

다음과 같은 경우 Pull Request의 Merge가 반려됩니다.

1. 알려지지 않은 Github ID일 경우
2. `pr` 타이틀 형식이 [Baekjoon] yy-mm-dd 이 아닐 경우
3. `pr` 이 생성된 날짜와 타이틀의 날짜가 다를 경우
4. `pr` 생성 시 본인 이름의 라벨이 없을 경우
5. `파일명`에 공백 또는 특수문자가 있는 경우
6. `파일명`이 숫자로 시작하는 경우 (ex. `1번상자_승열.py`)
7. `파일 경로`가 올바르지 않는 경우 (ex. `baekjoon/이상한폴더!/코드_최승열.py`)
8. `파일명`의 확장자가 없거나 올바르지 않는 경우 (ex. `.gitignore`)
9. `파일명`이 `문제명_이름` 형식으로 되어있지 않는 경우 (ex. `통학의신+승열.py`)
10. `파일명`에 제출자의 이름이 없거나 다른 이름이 있는 경우 (ex. `통학의신.py`)


다음과 같은 경우 Pull Request가 Merge가 실패처리 됩니다.

1. Merge Conflict가 있는 경우

## Pull 요청 검증 Flowchart

![스크린샷 2023-05-01 142823](https://user-images.githubusercontent.com/100273844/235411761-fff1dbf0-8488-497a-98ce-cdc0b534df24.png)

# GitHub

[https://github.com/danielchoi1115/gwichanhub](https://github.com/danielchoi1115/gwichanhub)

# Change Logs

## 23-04-30

### **`Mod`**

- Pull Request 타이틀에 공백이 있어도 반려처리되지 않도록 수정
## 23-04-24

### **`Bug`**

- Github 아이디의 대소문자가 다르면 인식하지 못하던 오류 수정

## 23-04-22

### `Feature`

- 제출하지 않은 사람의 이름도 출력하도록 변경

## 23-04-19

### `Bug`

- 파일 확장자의 대소문자가 다르면 인식하지 못하던 오류 수정
- 파일 확장자가 없을 때 예외 처리를 하지 못하던 오류 수정

## 23-04-15

### `Mod`

- 보고서에 이름을 오름차순으로 정렬한 뒤 출력하도록 수정

## 23-03-25

### `Bug`

- "H_" 로 시작하는 파일명을 정상적으로 인식하도록 수정

## 23-03-24

### `Feature`

- 파일이 올바른 폴더에 있는지 검사하는 기능 추가
- 오류가 발생했을 경우에도 오류메시지를 전송하는 기능 추가

### `Bug`

- 9시에 자동으로 실행이 되지 않던 오류 수정

## 23-03-23

### `Mod`

- Merge Request 이후 sleep 시간을 더 길게 조정

### `Bug`

- 알려지지 않은 github id가 검사될 경우 None 대신 id를 출력하도록 수정

## 23-03-21

### `Feature`

- 파일 경로를 검사하는 기능 추가

### `Mod`

- 보고서에 Pull Request Number 대신 이름을 출력하도록 변경
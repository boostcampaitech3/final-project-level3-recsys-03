# Git Ground Rule & Guide


## 선행작업
1. ~~develop branch를 만들기.~~
2. ~~kanban board 만들기.(완료)~~
--------------------------------
## Simple Guide
1. __새로운 feature branch를 만들 때에는__ 만들기 전에 __develop branch로 이동__ 후 만들어주세요.  
ex) ($ git checkout develop) 이후 ($git checkout -b frontend/login)  
   <img src="https://user-images.githubusercontent.com/78737997/167878257-c2ad09d5-fe84-440c-922e-a39f26269387.png" width="500" height="250">
  
  
  
2. __기능이 완성되었을 경우__ feature branch에 직접 merge 하는 것이 아닌 __branch를 원격에 push한 후 pull-request를 올려주세요.__   
만약 __기능이 완성되지 않았지만__ 다른 팀원들의 리뷰를 원해서 pull-request를 올리고 싶은 경우 __pull-request 제목에 'WIP'를__ 붙여주세요.  
커밋 메세지는 [Git - 커밋 메시지 컨벤션](http://asq.kr/y2RX19DXJ3)를 따릅니다.  
<img src="https://user-images.githubusercontent.com/78737997/167887078-92d51bfa-92a8-41a1-ba8d-1e35a6a571a9.png" width="400" height="200">   <img src="https://user-images.githubusercontent.com/78737997/167888138-b96e1d89-2618-4741-8f76-72f4c1bdf6b6.png" width="400" height="200">  



3. __pull-request가 완료__ 된 이후 본인이 사용했던 __feature branch는 삭제__ 해주세요.  
ex) ($git branch -D frontend/login) ($git push origin --delete frontend/login)


4. __다른 팀원이 완료한 pull-request가__ 있다면 local의 __develop branch를 동기화 하여 최신 상태를 유지__ 해주세요.  
ex) ($git checkout develop) ($git pull origin develop)  


----------------------------------
## 커밋 메시지 컨벤션

- 커밋 메시지 구조

```
type : subject

body

footer
```

- type 종류

| 커밋 타입 |   설명    |
| -------- | -------- |
| Feat     | 새로운 기능 추가 |
| Fix      | 버그 수정 |
| Docs     | 문서 수정 |
| Style    | 코드 포맷팅 등 코드 변경이 없는 경우 |
| Refactor | 코드 리팩토링, 새로운 기능이나 버그 수정없이 현재 구현을 개선한 경우 |
| Test     | 테스트 코드 추가 |
| Remove   | 사용하지 않는 파일 혹은 폴더를 삭제하는 경우 

- subject

    - 제목은 50자를 넘기지 않고, 한글로 통일한다.
    - 동사를 앞에 쓰며 과거시제를 사용하지 않고 명령어로 작성한다.
        - "XX화면에서 버그를 수정했음" -> "수정 XX화면 버그"
        - "테스트 코드 추가했음" -> "추가 테스트 코드"
    - 제목 끝에 마침표(`.`)를 붙이지 않는다.
    - 제목과 본문은 띄어쓴다.

- body

    - 어떤 것을 수정했는지에 대한 내용을 작성한다.
    - 작성할 때는 "How"보다 "What"과 "Why"를 적도록 한다.

- footer

    - 선택사항이며, issue 와 관련된 내용이 있다면 사용한다.
----------------------------------
## 브랜치 관리


- Master
    - 데모 가능한 상태의 브랜치.

- Develop
    - merge 하게 될 브랜치.

- Feature
    - 기능별로 여러 브랜치를 생성한다. ex) feature/forntend/login

- Hotfix
    - 계획에 없는 버그 발견 시 급하게 처리해야 할 일.
------------------------------------
## PR
- PR 구조
    - (만약 커밋이 여러개 일 경우) 제목 : `[클래스명 #Issue번호] PR 제목(subject1, subject2 ... )`  
      ex) [Backend] 서버 배포작업 추가, 기타 오류 수정
    - (만약 커밋이 하나 일 경우) 제목 : `commit subject`  
      ex) fix: "추가 로그인 기능"
    - 내용 : issue를 어떻게 해결했는가, 해결하면서 어떤 점이 어려웠는가 등 쓰고 싶은 내용을 쓰도록 한다.
- Assignees, Label, Milestone를 체크해놓는다.
- PR에 대한 Assignees의 approve가 모두 있을 경우에만 merge가 가능하도록 한다.
------------------------------------
## 이슈 및 마일스톤 관리
- 이슈는 최대한 작은 단위(WBS)로 분리하여 발행한다. 
    - 추후 너무 작은 단위라고 느낄 때 기능 단위로 합치도록 한다.
- 버전마다 마일스톤을 새롭게 생성하여 먼저 처리해야 할 이슈들을 구분하고, 기능 목록을 각자 할 일 단위로 쪼개서 관리해야 한다.



----------------------------
## Pull-Request Guide
1. feature branch를 develop branch와 pull request 할 때 __base가 develop branch가 맞는지__ 확인해주세요.
   <img src="https://user-images.githubusercontent.com/78737997/167996988-66db7c13-64fe-4fe8-8024-71cbdd6ffc4e.png" width="500" height="250">
2. feature branch의 기능이 하나인 경우 제목은 commit 제목과 동일하게, 여러 개인 경우 [클래스] 추가한 기능들을 제목으로 적어주세요.  
   ex) [Backend] docstring 추가, 연동 기능 추가  
   <img src="https://user-images.githubusercontent.com/78737997/167997438-ecb44df1-aa50-4921-8f19-9c7e9d6194d2.png" width="500" height="250">
   - Reviewers는 해당 branch와 연관 있는 사람을 선택해주세요.
   - Assigness는 본인을 넣어주세요.
   - Lables는 관련 있는 태그를 선택해주세요. 여러 개 선택해주셔도 괜찮습니다.
   - Projects를 선택해주시면 프로젝트 칸의 In progress에 자동으로 들어갑니다.
   - Milestone에 해당 기능이 어떤 버전에 들어가는지 선택해주세요.  
3. 다른사람 pull-request를 리뷰를 할 때 수정한 파일들을 확인한 후 __수정 할 부분이 있으면 코멘트를__ 남겨주세요.  
   <img src="https://user-images.githubusercontent.com/78737997/167999613-010a3b9c-229d-4cb7-b63e-e51bab9df2c6.png" width="400" height="200">  
   <img src="https://user-images.githubusercontent.com/78737997/168005557-c720652e-97e1-4f78-b59d-d718c2f64e03.png" width="400" height="200">  
   ```
   수정이 필요한 줄에 '+' 버튼을 눌러서 댓글을 남겨주세요.
   더 많은 수정이 필요할 경우 'start a review' 버튼을, 아닌 경우 'add single comment를 눌러주세요.
   ```
   <img src="https://user-images.githubusercontent.com/78737997/168005843-a0f166cf-bc93-462d-8386-c1165a36a7a6.png" width="400" height="200">  
   
   `확인이 끝난 경우 어떤 것을 확인했는지 적어 주시고 제출해주시면 됩니다.`


   - 확인할 사항
      - feature 브랜치에서 develop 브랜치로 pull-request 신청하는 것이 맞는지
      - commit 제목과 수정사항이 일치하는지 
      - 변수명 또는 함수명은 적절한지
      - 다른 파일 또는 기능과 충돌할 사항은 없는지
      - label 또는 issue 항목은 적절한지
------------------------------
## Issue Guide
1. 제안사항, 궁금증, bug, hotfix 등등 Issue가 있을 때 작성해주세요.  
   <img src="https://user-images.githubusercontent.com/78737997/168001669-50ddf76b-5bbd-4613-85a8-32f8d8a8c1e4.png" width="500" height="250">
   - Assigness는 담당 팀원을 넣어주세요.(해당 팀원에게도 알려주세요.)
   - Lables는 관련 있는 태그를 선택해주세요. 여러 개 선택해주셔도 괜찮습니다.
   - Projects를 선택해주시면 프로젝트 칸의 To do 에 자동으로 들어갑니다.
   - Milestone에 해당 기능이 어떤 버전에 들어가는지 선택해주세요.(만약 아직 예정된 버전이 없다면 새 마일스톤을 만들어주시거나 비워두시고 이후 수정해도 괜찮습니다)
2. issue에서 댓글로 자유롭게 토의해도 좋습니다 :)
## Project Guide
1. To-do 에는 Issue들, In progress와 Review in progress에는 Pull-request들을 확인할 수 있습니다.
   <img src="https://user-images.githubusercontent.com/78737997/168003618-afa42230-4946-4630-b384-7d0946c476db.png" width="400" height="200">  <img src="https://user-images.githubusercontent.com/78737997/168004064-e0662d33-b219-44c2-af45-d65ef7995496.png" width="400" height="200">  
   - Pull-request를 작성하실 때 Issue number를 활용하셔도 좋습니다👍
   - __Pull-request를 작성 한 이후에는 To-do 항목에서 관련 Issue를 지워주세요.__
   - 완료된 Pull-request의 경우 Done으로 옮겨주세요.


----------------------------
## FAQ(자주 하는 실수)
- commit message를 잘 못 올렸습니다.(원격 저장소에 branch를 푸쉬 하기 전, 본인이 마지막으로 올린 커밋 메세지만 가능)
  - ($ git commit --amend) 후 필요한 메세지를 수정 후 :wq 로 저장
- 마지막으로 올린 commit을 취소하고 싶어요.(원격 저장소에 branch를 푸쉬 하기 전)
  - [방법 1] commit을 취소하고 해당 파일들은 staged 상태로 워킹 디렉터리에 보존  
  ($ git reset --soft HEAD^)
  - [방법 2] commit을 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉터리에 보존  
  ($ git reset HEAD^)  
  - [방법 3] commit을 취소하고 해당 파일들은 unstaged 상태로 워킹 디렉터리에서 삭제  
  ($ git reset --hard HEAD^)  
  - 만약 커밋이 하나가 아니라 여러개라면?  
    ($ git reset HEAD~2) : 마지막 2개의 commit을 취소
- 깃을 사용하다가 제가 작업한 파일들이 날라갔어요. 되돌릴 수 있는 방법이 있을까요??
  - ($ git reflog) 로 원하는 commit ID를 확인 후 
  - ($ git checkout {commit ID})를 사용해서 되돌리기

## ETC
- __($ git push --force)는 최대한 지양해주세요.__ 혹시 사용할 일이 있으면 팀원들에게 물어본 후 사용해주세요.
- 언제든 궁금한 내용이 있으면 Slack에 물어봐주세요.

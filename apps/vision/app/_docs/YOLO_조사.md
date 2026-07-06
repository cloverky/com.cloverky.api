# YOLO 조사

> 출처: Evernote 노트 (컴퓨터비전 / YOLO 조사)

---

## 목차

1. Object Detection(객체 검출)의 역사
2. Object Detection(객체 검출)의 방식
3. YOLO의 정의
4. CNN계열 Fast R-CNN과 YOLO의 비교
5. YOLO의 발전과정
6. YOLO 조사결과와 의견

---

## 1. Object Detection(객체 검출)의 역사

객체 검출은 카메라나 다른 센서를 이용하여 자동차, 사람, 동건 등을 검출하는 것이다.

컴퓨팅파워가 좋아지기 전에는 문제를 모두 영상처리로 풀고 있다가, 2012년 AlexNet 이후부터는 딥러닝을 활용하여 문제를 접근하고 있다.

영상처리는 정적인 상태를 인식한다. 따라서 하나의 이미지에서 객체 검출을 위한 영역분할을 한다. 하나의 윈도우로 물체를 인식하는 것은 알고리즘의 성능이 좋지 않았고, 지정된 객체의 인식과 대상 조작에 있어서 정확도가 많이 떨어졌다.

이를 해결하기 위해 동적인 상태인식을 통해 가상의 깊이를 정의하도록 시도했다. 다계층 중첩 윈도우를 사용하여 다계층 중첩 윈도우 영역 간의 교차영역을 지정해 정확도를 올릴 수 있었다. 근래에는 밀집한 소형 물체의 정확한 위치 검출을 위한 다계층 중첩 윈도우를 이용한 네트워크의 성능개선이 이뤄지고 있다.

---

## 2. Object Detection(객체 검출)의 방식

객체 검출 방식에는 크게 **Two-shot detection**과 **One-shot detection** 2가지가 있다.

### Two-shot Detection (2단계 검출)

대표 신경망: **R-CNN**

1. RPN(Region Proposal Network)으로 예상범위 추출 작업을 한다.
   - Selective Search 알고리즘으로 추려낸 수많은 박스 중 비슷한 위치의 박스들을 줄여 임의 랜덤사이즈 Bounding Box만 남긴다.
2. 모든 Bounding Box들을 CNN으로 보낸다.
   - 몇 번의 네트워크를 통과해야 하므로 연산량이 상당히 많다.

### One-shot Detection (1단계 검출)

input image가 있으면 하나의 신경망을 통과하여 물체의 Bounding Box와 Class를 동시에 예측하는 방식.

대표 모델: **YOLO**, SSD, RetinaNet

- **장점**: 합성곱 신경망을 단 한 번 통과하므로 임의의 상품에 대해서 피팅이 가능
- **단점**: 학습 정도와 이미지 크기에 따라 모델의 성능이 크게 달라짐

---

## 3. YOLO의 정의

**YOLO** = **Y**ou **O**nly **L**ook **O**nce의 약어

Joseph Redmon이 워싱턴 대학에서 여러 동료들과 함께 2015년에 YOLOv1을 처음 논문으로 발표했다.

당시 Object Detection에서 가장 좋은 성능을 내던 **Faster R-CNN(Region with Convolutional Neural Network)** 을 대체하는 **One-shot detection** 방법을 처음으로 고안하였다.

기존 CNN 계열은 Two-shot-detection으로 Object Detection을 구성하여 실시간성이 굉장히 부족하다는 단점이 있었다.

---

## 4. CNN계열 Fast R-CNN과 YOLO의 비교

| 항목 | 내용 |
|------|------|
| 속도 | R-CNN → Fast R-CNN → Faster R-CNN → YOLO 는 대략 **10배씩** 속도 차이가 난다 |
| YOLO 성능 | YOLO 등장으로 **45 FPS**, 빠른 버전은 더 높은 프레임 기록 |
| YOLO 단점 | 학습 정도와 이미지 크기에 따라 모델 성능이 크게 달라짐, 겹쳐 있는 상태에 대한 예측이 불확실 |
| Fast R-CNN 단점 | 높은 이미지 분류 정확도이나 과도한 오버헤드 발생, 시간 소모, 현실 적용에 무용한 상태 |

---

## 5. YOLO의 발전과정

### YOLOv1

1. 네트워크 구조는 이미지 분류를 위해 설계된 **GoogLeNet** 모델 기반
2. 24개의 컨볼루션 계층과 2개의 완전히 연결된(Fully Connected) 계층으로 구성
3. 풀링 계층은 사용하지 않음

---

### YOLOv2

1. 대량의 분류 데이터를 활용하기 위해 고안된 방법
2. YOLOv1에 비해 정확도와 속도 향상을 위해 **일괄 정규화(Batch Normalization) 계층** 추가
3. 경계 박스의 예측을 완전히 연결된 계층 대신에 **앵커박스(Anchor Box)**에서 수행하여 네트워크를 축소하면서 출력 해상도를 향상

---

### YOLOv3

1. **로지스틱 회귀(Logistic Regression)** 를 적용하여 경계 박스의 객관성 점수(Objectness Score)를 예측
2. 경계 박스 예측, 클래스 예측, 특징 검출기 및 반복적 검출 방지를 개선
3. 결합된 특징 맵을 처리하고 보다 큰 텐서를 예측하기 위해 추가적인 컨볼루션 계층 포함

---

### YOLOv4

1. YOLOv3 이후에 나온 딥러닝의 정확도를 개선하는 다양한 방법을 적용해 YOLO의 성능을 극대화하는 방법 구현
2. 대표적인 모듈인 **SPP(Spatial Pyramid Pooling)** 는 딥러닝에 최적화하기 위해 CNN과 SPM을 결합하고 bag-of-words 대신 max pooling을 사용
3. 테스트 성능 결과: 기존 v3 대비 약 **7% 추론시간 증가**, **5.7% 정확도 향상**

---

### YOLOv5

1. YOLOv3를 **PyTorch**로 구현(implementation)한 모듈
2. FPS와 mAP 측면에서 모두 뛰어난 성능 발휘
3. 아키텍처에 **CSPNet(BottleneckCSP)** 적용
   - 논문 제목: *CSPNET: A NEW BACKBONE THAT CAN ENHANCE LEARNING CAPABILITY OF CNN*
   - CNN의 학습 능력을 향상시킬 수 있는 새로운 백본으로 정의

---

## 6. YOLO 조사결과와 의견

최근 객체 검출 분야에서 딥러닝 알고리즘은 없어서는 안 되는 중요한 요소이다. 이들 중에서 **YOLO 네트워크는 딥러닝 네트워크의 단점인 느린 처리속도를 획기적으로 줄임**으로써 주목받고 있다.

데이터의 공급이 인공지능의 성능을 올리는 포커스임은 분명하다. 이론에 머무르지 않고, 현실에 바로 적용 가능한 신경망 메소드를 통해 동적 이미지 인식의 방법을 이해할 수 있었다.

하지만 YOLO 네트워크는 다른 딥러닝 알고리즘에 비해 **검출율이 비교적 낮다**는 단점을 가지고 있다. 특히 소형 오브젝트에 대해서는 더욱 검출 성능이 낮아진다는 의견이 많다.

**향후 발전 방향 예측**: YOLO 네트워크가 갖고 있는 소형 물체의 높은 미검출이나 밀집된 상황에서의 오검출 등의 단점을 개선하기 위해, **다계층 중첩 윈도우 기반 알고리즘**으로 진화하는 것으로 예측된다.

---

## 주요 논문 출처 및 참고 자료

1. **객체검출의 역사**
   - *Object Detection in 20 Years: A Survey*
   - https://arxiv.org/pdf/1905.05055.pdf

2. **Object Detection 방식 참고**
   - https://mickael-k.tistory.com/24?category=798521

3. **밀집한 소형 물체의 정확한 위치 검출을 위한 다계층 중첩 윈도우를 이용한 YOLO 네트워크의 성능개선**
   - 저자: 유재형, 한영준, 한헌수

4. **객체 검출을 위한 CNN과 YOLO 성능 비교 실험**
   - 원광대학교 디지털콘텐츠공학과, 이용환, 김영섭

5. *VITON: An Image-based Virtual Try-on Network*

6. *Self-Correction for Human Parsing*, Peike Li et al.

7. *Devil in the Details: Towards Accurate Single and Multiple Human Parsing*

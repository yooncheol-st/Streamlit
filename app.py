
import random
import base64
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def init_page():
    st.set_page_config(
        page_title="오늘 뭐 먹지?",
        page_icon="🍽️"
    )

    st.title("🍽️ 오늘 뭐 먹지?")
    st.markdown(
        "GPT가 오늘 먹으면 좋을 음식을 추천하고 "
        "애니메이션 스타일 이미지까지 생성해드립니다."
    )


def recommend_food():

    response = client.responses.create(
        model="gpt-5",
        input="""
        오늘 먹으면 좋을 음식 후보 20개를 추천해줘.

        조건:
        - 한국 음식
        - 일본 음식
        - 중국 음식
        - 양식

        다양하게 섞어줘.

        음식 이름만 출력해.
        한 줄에 하나씩 작성.
        번호 금지.
        """
    )

    foods = []

    for line in response.output_text.split("\n"):
        line = line.strip()

        if line:
            foods.append(line)

    return random.choice(foods)


def generate_food_image(food):

    response = client.images.generate(
        model="gpt-image-2",
        prompt=f"""
        {food}

        일본 애니메이션 스타일. (인물은 나오지 않게)

        음식이 매우 맛있어 보이는 장면.

        밝고 따뜻한 분위기.

        """
    )

    image_bytes = base64.b64decode(
        response.data[0].b64_json
    )

    return image_bytes



def main():

    init_page()

    st.markdown("---")

    if st.button("🎰 룰렛 돌리기"):

        with st.spinner("GPT가 메뉴를 추천하는 중..."):

            food = recommend_food()

        st.success(
            f"🎯 오늘의 추천 메뉴 : {food}"
        )

        with st.spinner("이미지 생성 중..."):

            image = generate_food_image(food)

        st.image(
            image,
            caption=food,
            use_container_width=True
        )

main()


import os
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import chain


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class Image(BaseModel):
    format: str
    b64: str


class ClassifiedAd(BaseModel):
    id: str
    user_id: str
    title: str
    description: str
    images: Optional[List[Image]]


class ImageInfo(BaseModel):
    tags: List[str]
    description: str
    people_count: int
    has_explicit_content: bool


class ClassifiedAdEnriched(ClassifiedAd):
    images_info: List[ImageInfo]
    category: str
    summary: str


@chain
def image_model(inputs):
    model = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        temperature=0.5,
        model="gpt-4o",
        max_tokens=1024
    )
    img_prompt = PromptTemplate(template="""
    Given the image, provide the following information:
    - A list of descriptive tags of the main objects in the image 
     (between 5 - 10 tags)
    - A short description of the image
    - The number of people in the image
    - Whether the image has explicit content or not
    
    {format_instructions}
    """)
    img_message = img_prompt.format(
        format_instructions=inputs["format_instructions"]
    )
    img_fmt = inputs['image'].format
    img_b64 = inputs['image'].b64
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": img_message},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_fmt};base64,{img_b64}"}
                    }
                ]
            ),
        ]
    )
    return msg.content


@chain
def ad_model(inputs: dict):
    model = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        temperature=0.5,
        model="gpt-4o",
        max_tokens=1024
    )

    ad = inputs["ad"]
    images_info = inputs["images_info"]

    images_info_str = ""
    if len(images_info) > 0:
        images_info_str = """
        - Images:
        """
        for img in images_info:
            images_info_str += f"\n- {img}"

    ad_prompt = PromptTemplate(template="""
        Give the following classified ad information:
        - Ad ID: {id}
        - User ID: {user_id}
        - Title: {title}
        - Description: {description}
        {image_descriptions} 
        
        Available ad categories:
            - car, bike and boats
            - services
            - event tickets
            - electronics
            - home and garden
            - jobs
            - property
            - fashion & beauty
            - music, films and books
            - courses and lessons
            - give away and exchange
            
        Write a short summary of the classified ad and classify the ad in one of 
        the available ad categories.
        
        {format_instructions}
        """)

    message = ad_prompt.format(
        format_instructions=inputs["format_instructions"],
        id=ad.id,
        user_id=ad.user_id,
        title=ad.title,
        description=ad.description,
        image_descriptions=images_info_str
    )

    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": message},
                ]
            ),
        ]
    )
    return msg.content


def handler(data, logs):
    """
    data is a json with a classified ad data:

    {
        "title": "",
        "description": "",
        "images": [
            {
                "format": "image/png",
                "b64": ""
            },
            {
                "format": "image/png",
                "b64": ""
            }
        ]
    }
    """
    ad_data = ClassifiedAd(**data)

    logs.info("Processing Ad images...")
    images_info = []
    if ad_data.images and len(ad_data.images) > 0:
        image_parser = JsonOutputParser(pydantic_object=ImageInfo)
        image_chain = image_model | image_parser

        for img in ad_data.images:
            img_info = image_chain.invoke(input={
                "image": img,
                "format_instructions": image_parser.get_format_instructions()
            })
            images_info.append(img_info)
            logs.debug(f"Image info: {img_info}")

    logs.info("Processing Ad...")
    ad_parser = JsonOutputParser(pydantic_object=ClassifiedAdEnriched)
    ad_chain = ad_model | ad_parser

    return ad_chain.invoke(input={
        "ad": ad_data,
        "images_info": images_info,
        "format_instructions": ad_parser.get_format_instructions()
    })

from lv.entities.classification import Classification


async def post_classification(
    classification_data: Classification, email: str
) -> None:
    # DI 를 쓰지 않는다면, 이 service 를 call 하는 presentation func 에서
    # repo 넘겨주고, 받을 때 type 을 repo_interface 로 받는다

    # 엔티티를 두개의 json 으로 쪼갬
    # classification table & academic info
    # await classification_repo.insert(json1 + email)
    # await academic_repo.insert(json2 + email)
    pass

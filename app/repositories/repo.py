from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from aiwrappifymodels.rehearse_curate import Status
from app.models.sqlalchemy.models import TopicRecord, CuratedFileRecord
from app.repositories.base import BaseRepo
from motionggrpcutils.exceptions.base import CustomException
from google.protobuf.field_mask_pb2 import FieldMask
from aiwrappifymodels.rehearse_curate import CuratedFile, Topic, TopicCreate, TopicPatch, CuratedFileCreate, CuratedFilePatch
from aiwrappifymodels.utils import decompose_name_to_ids
class SqlAlchemyTopicRepo(BaseRepo):
    def __init__(self, db: Session):
        self.db = db

    def create(self, topic: TopicCreate):
        db_item = TopicRecord(
            display_name=topic.display_name,
            description=topic.description,
            message_event_id=topic.message_event_id,
            agent_id=topic.agent_id,
            machine_curation_status=topic.machine_curation_status,
            human_curation_status=topic.human_curation_status,
        )
        try: 
            self.db.add(db_item)
            self.db.flush()
        except Exception as e:
            raise CustomException(code=400, message=f"Failed to create channel:{e}")
        return Topic.model_validate(db_item, from_attributes=True)

    def get_one(self, id: str):
        db_item=self.db.query(TopicRecord).filter(Topic.id == id).first()
        if db_item is None:
            raise CustomException(code=404, message="Topic not found")
        return Topic.model_validate(db_item, from_attributes=True)

    def patch_one(self, topic_patch:TopicPatch, field_mask:FieldMask):
        topic_id, = decompose_name_to_ids(topic_patch.name) 
        db_item=self.db.query(TopicRecord).filter(Topic.id == topic_id).first()
        if db_item is None:
            raise CustomException(code=404, message="Topic not found")
        for field in field_mask.paths:
            setattr(db_item, field, getattr(topic_patch, field))
        try:
            self.db.flush()
        except Exception as e:
            raise CustomException(code=400, message=f"Failed to update channel:{e}")
        return Topic.model_validate(db_item, from_attributes=True)

    
    # def update_status_to_digested(self, id: str):
    #     self.db.query(Topic).filter(Topic.id == id).update(
    #         {Topic.is_digested: True, Topic.digested_time: datetime.now(timezone.utc)}
    #     )

    # def update_machine_curation_status(self, id: str, status: Status):
    #     self.db.query(Topic).filter(Topic.id == id).update({Topic.machine_curation_status: status})

    # def update_human_curation_status(self, id: str, status: Status):
    #     self.db.query(Topic).filter(Topic.id == id).update({Topic.human_curation_status: status})


class SqlAlchemyCuratedFileRepo(BaseRepo):
    def __init__(self, db: Session):
        self.db = db

    def create(self, curated_file: CuratedFile):
        db_item = CuratedFileRecord(
            storage_uri=curated_file.storage_uri,
            topic_id=curated_file.topic_id,
            digest_status=curated_file.digest_status,
            source=curated_file.source,
            human_raw_response_id=curated_file.human_raw_response_id,
        )
        try:
            self.db.add(db_item)
            self.db.flush()
        except Exception as e:
            raise CustomException(code=400, message=f"Failed to create curated file:{e}")
        return CuratedFile.model_validate(db_item, from_attributes=True)

    def get_one(self, id: str):
        db_item=self.db.query(CuratedFileRecord).filter(CuratedFile.id == id).first()
        if db_item is None:
            raise CustomException(code=404, message="Curated file not found")
        return CuratedFile.model_validate(db_item, from_attributes=True)

    def patch_one(self, curated_file_patch:CuratedFilePatch, field_mask:FieldMask):
        curated_file_id, = decompose_name_to_ids(curated_file_patch.name) 
        db_item=self.db.query(CuratedFileRecord).filter(CuratedFile.id == curated_file_id).first()
        if db_item is None:
            raise CustomException(code=404, message="Curated file not found")
        for field in field_mask.paths:
            setattr(db_item, field, getattr(curated_file_patch, field))
        try:
            self.db.flush()
        except Exception as e:
            raise CustomException(code=400, message=f"Failed to update curated file:{e}")
        return CuratedFile.model_validate(db_item, from_attributes=True)

        
    def get_files_by_topic(self, topic_id: str):
        db_items=self.db.query(CuratedFileRecord).filter(CuratedFile.topic_id == topic_id).all()
        return [CuratedFile.model_validate(db_item, from_attributes=True) for db_item in db_items]
        


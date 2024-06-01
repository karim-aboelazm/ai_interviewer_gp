from pathlib import Path
from affinda import AffindaAPI, TokenCredential
from affinda.models import CollectionCreate, WorkspaceCreate
import random
import string


def get_resume_info(resume_path: str = None, token: str = None):
    random_text = ''.join(random.choices(string.ascii_lowercase, k=6))
    file_pth = Path(resume_path)
    credential = TokenCredential(token=token)
    client = AffindaAPI(credential=credential)
    my_organisation = client.get_all_organizations()[0]
    existing_workspaces = client.get_all_workspaces(organization=my_organisation.identifier)
    workspace_name = "My Workspace"
    workspace_number = 1
    while any(workspace.name == workspace_name for workspace in existing_workspaces):
        workspace_name = f"My Workspace {workspace_number}"
        workspace_number += 1

    # Create the workspace
    workspace_body = WorkspaceCreate(
        organization=my_organisation.identifier,
        name=workspace_name,
    )
    recruitment_workspace = client.create_workspace(body=workspace_body)
    collection_body = CollectionCreate(name=random_text, workspace=recruitment_workspace.identifier, extractor="resume")
    resume_collection = client.create_collection(collection_body)
    with open(file_pth, "rb") as f:
        resume = client.create_document(file=f, file_name=file_pth.name, collection=resume_collection.identifier)
    res = resume.as_dict()['data']
    work_experience = res['work_experience']
    all_works = []
    for work in work_experience:
        all_works.append({'job_title': work['job_title'],
                          'organization': work['organization'],
                          'duration': f"From {work['dates']['start_date']} - To {work['dates']['end_date']}"})
    skills = res['skills']
    all_skills = [skill['name'] for skill in skills]

    resume_data = {
        "full_name": res['name']['raw'],
        "email_address": res['emails'],
        "phone_number": res['phone_number_details'][0]['formatted_number'],
        "links": res['websites'],
        "date_of_birth": res['date_of_birth'],
        "address": res['location']['raw_input'],
        "education": f"{res['education'][0]['accreditation']['input_str']} - {res['education'][0]['organization']} - {res['education'][0]['dates']['raw_text']}",
        "total_experience": res['total_years_experience'],
        "languages": res['languages'],
        "profession": res['profession'],
        "work_experience": all_works,
        "skills": all_skills
    }
    return res, resume_data

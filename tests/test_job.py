import datetime
from scraper.base_class import Job

job_1 = Job(
    "Python Dev",
    "München",
    "Fivver",
    "Best Job ever",
    "www.jobgy.com",
    datetime.date(2022, 2, 3),
)
job_2 = Job(
    "Python Dev",
    "München",
    "Fivver",
    "Best Job ever",
    "www.jobgy.com",
    datetime.date(2022, 2, 3),
)
job_3 = Job(
    "C++ Dev",
    "München",
    "Fivver",
    "Best Job ever",
    "www.jobgy.com",
    datetime.date(2022, 2, 3),
)


def test_eq():
    assert job_1 == job_2
    assert job_1 != job_3


def test_hash():
    assert len(set([job_1, job_2, job_3])) == 2


def test_str():
    assert (
        str(job_1)
        == f"Title={job_1.title} Location={job_1.location} Company={job_1.company}"
    )

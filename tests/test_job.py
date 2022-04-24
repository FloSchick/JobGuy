from scraper.jobsearch import Job

job_1 = Job("Python Dev", "München", "Fivver", "Best Job ever", "www.jobgy.com")
job_2 = Job("Python Dev", "München", "Fivver", "Best Job ever", "www.jobgy.com")
job_3 = Job("C++ Dev", "München", "Fivver", "Best Job ever", "www.jobgy.com")


def test_eq():
    assert job_1 == job_2
    assert job_1 != job_3


def test_str():
    assert (
        str(job_1)
        == f"Title={job_1.title} Location={job_1.location} Company={job_1.company}"
    )

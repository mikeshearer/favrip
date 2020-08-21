from favrip.models.domain import Domain

def test_domain_sort():
	domain1 = Domain(1, "google.com")
	domain2 = Domain(2, "facebook.com")
	domains = [domain2, domain1]
	domains.sort()

	assert domains == [domain1, domain2]

def test_domain_lt():
	domain1 = Domain(1, "google.com")
	domain2 = Domain(2, "facebook.com")

	assert domain1.__lt__(domain2)


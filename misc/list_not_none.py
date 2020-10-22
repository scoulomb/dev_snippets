from typing import Any, List, Optional


# Some ideas here:
# - https://stackoverflow.com/questions/8826521/python-avoiding-if-condition-for-this-code
# - https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
# 281 lb

def v1():
    profiles: List[Any] = []

    tcp_client_profile: Optional[str] = "tcp"  # "tcp", with comma is tuple when not in func args!
    http_profile: Optional[str] = "http"
    client_ssl_profile: Optional[str] = None

    if tcp_client_profile is not None:
        profiles.append(tcp_client_profile)
    if http_profile is not None:
        profiles.append(http_profile)
    if client_ssl_profile is not None:
        profiles.append(client_ssl_profile)

    print(profiles)


def v2():
    tcp_client_profile: Optional[str] = "tcp"  # "tcp", with comma is tuple when not in func args!
    http_profile: Optional[str] = "http"
    client_ssl_profile: Optional[str] = None

    profiles = [tcp_client_profile, http_profile, client_ssl_profile]
    # print(profiles)
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    filtered_profiles = [profile for profile in profiles if profile != None]
    print(filtered_profiles)


def v3():
    tcp_client_profile: Optional[str] = "tcp"  # "tcp", with comma is tuple when not in func args!
    http_profile: Optional[str] = "http"
    client_ssl_profile: Optional[str] = None

    profiless = [tcp_client_profile, http_profile, client_ssl_profile]
    # print(profiles)
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    filtered_profiles = list(filter(lambda profile: profile is not None, profiless))
    print(filtered_profiles)


def v4():
    tcp_client_profile: Optional[str] = "tcp"  # "tcp", with comma is tuple when not in func args!
    http_profile: Optional[str] = "http"
    client_ssl_profile: Optional[str] = None

    profiles = [tcp_client_profile, http_profile, client_ssl_profile]
    # print(profiles)
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    filtered_profiles = list(filter(None, profiles))
    print(filtered_profiles)


v1()
v2()
v3()
v4()

import sys
import os

# this should be before import. need to solve linter rule. so added # noqa
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                '/../python_modules') # noqa

from member import get_member_status


def display_members(members):
    if (len(members)) == 0:
        print("member does not exist")

    for member in members:
        print("==============")
        print("member for email : ", member.email)
        print("member exists")
        print("status : ", member.member_status)
        print("type : ", member.member_type)
        print("password last change date : ",
              member.password_last_change_date)


# tests
found_members = get_member_status('aaa@email.com')
display_members(found_members)

found_members = get_member_status('mmm@email.com')
display_members(found_members)

found_members = get_member_status('aaas49807@email.com')
display_members(found_members)

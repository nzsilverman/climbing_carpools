""" Climbing Carpool generator. """
import read_responses

def main():
    form_responses = read_responses.generate_response_lists()
    tues_drivers = form_responses[0]
    tues_riders = form_responses[1]
    thurs_drivers = form_responses[2]
    thurs_riders = form_responses[3]
    sun_drivers = form_responses[4]
    sun_riders = form_responses[5]

    print("tues_drivers")
    print(tues_drivers)

    print("tues_riders")
    print(tues_riders)

    print("thurs_drivers")
    print(thurs_drivers)

    print("thurs_riders")
    print(thurs_riders)

    print("sun_drivers")
    print(sun_drivers)

    print("sun_riders")
    print(sun_riders)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()

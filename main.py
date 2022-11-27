'''
Algorithm to help during gas flow measurement performed with Log-Chebyshev method.

The program needs the following data before beginning of the main measurement:
- Temperature of measured gas [Celsius degree].
    Measurement of gas temperature inside the duct is made with a thermocouple
- Ambient pressure [hPa]
    Data obtained from archived weather data
- Static pressure [Pa]
    Measurement of static pressure inside the duct is made with Prandtl tube
- Prandtl tube coefficient depends on geometry of the device
    (0.81 for straight tube and 1.0 for curved tube)
- Diameter of the duct is measured with a caliper or similar tool
- Measurement accuracy (3 to 5 measurements per radius of the duct)

To measure pressure of gas, the user have to insert Prandtl tube inside the duct in few specific depths,
which are calculated by the algorithm. Pressure measured inside few
points inside the duct must be entered into the program.
Then algorithm calculate mass flow or volume flow in unit selected by the user.
'''

import math


def interface():
    print("Required data: \n"
          "0 - Calculation start \n"
          "1 - Gas temperature \n"
          "2 - Ambient pressure \n"
          "3 - Static pressure inside the duct \n"
          "4 - Prandtl tube coefficient \n"
          "5 - Diameter of the duct \n"
          "6 - Measurement accuracy \n")


def interface_result():
    print("Select unit of the result: \n"
          "0 - End of calculations \n"
          "1 - m3/s \n"
          "2 - m3/min \n"
          "3 - m3/h \n"
          "4 - kg/s \n"
          "5 - kg/min \n"
          "6 - kg/h \n")


def action_func():
    while True:
        action = int(input("What do you want to do [0-6]: "))
        if 0 <= action <= 6:
            break
        print("Action out of range \n"
              "Try again \n")
    return action


def answer_axis_func():
    while True:
        answer = int(input("Do you want to measure pressure inside the duct along one axis or two? (1/2): "))
        if 1 <= answer <= 2:
            break
        print("Wrong answer \n"
              "Try again \n")
    return answer


def temperature_func():
    while True:
        temperature = float(input("Enter gas temperature in Celsius: "))
        if temperature > -273.15:
            break
        print("Do not try to break law of physics \n"
              "Try again! \n")
    return temperature


def ambient_pressure_func():
    ambient_pressure = float(input("Enter ambient pressure [hPa]: "))
    return ambient_pressure


def static_pressure_func():
    static_pressure = float(input("Enter static pressure inside the duct [Pa]: "))
    return static_pressure


def prandtl_coef_func():
    prandtl_tube_coef = float(input("Enter prandtl tube coefficient: "))
    return prandtl_tube_coef


def duct_diameter_func():
    while True:
        duct_diameter = int(input("Enter diameter of the duct [mm]: "))
        if duct_diameter > 0:
            break
        print("Value of diameter must be higher than zero. \n"
              "Try again! \n")
    return duct_diameter


def measurement_accuracy():
    while True:
        accuracy_choice = int(input("Chose number of measurements per duct radius [3-5]: "))
        if 3 <= accuracy_choice <= 5:
            break
        print("Choice out of range \n"
              "Try again \n")
    return accuracy_choice


def accuracy_coef_func(accuracy_choice):
    accuracy_coef = tuple()
    if accuracy_choice == 3:
        accuracy_coef = (0.375, 0.925, 0.936)
    elif accuracy_choice == 4:
        accuracy_coef = (0.331, 0.612, 0.800, 0.952)
    elif accuracy_choice == 5:
        accuracy_coef = (0.287, 0.570, 0.689, 0.847, 0.962)
    return accuracy_coef


def measurement_points_func(accuracy_coef, duct_diameter):
    measurement_points = []
    for i in range(len(accuracy_coef)):
        position = round((duct_diameter/2)*accuracy_coef[i])
        measurement_points.append((duct_diameter/2) + position)
        measurement_points.append((duct_diameter/2) - position)
    measurement_points.sort()
    return measurement_points


def pressure_measurement_func(measurement_points):
    pressure_measurement = []
    for i in range(len(measurement_points)):
        print(i + 1, ". Measurement coordinate: ", measurement_points[i], " mm")
        pressure = int(input())
        pressure_measurement.append(pressure)
    return pressure_measurement


def absolute_pressure_func(static_pressure, ambient_pressure):
    absolute_pressure = (ambient_pressure * 100) + static_pressure
    return absolute_pressure


def density_func(temperature, absolute_pressure):
    density = 1.2928 * (absolute_pressure/101325) * (273.15/(273.15 + temperature))
    return density


def velocity_calculation(temperature, absolute_pressure, prandtl_tube_coef, pressure):
    velocity_list = []
    for i in range(len(pressure)):
        velocity = prandtl_tube_coef * (math.sqrt((573.87 * temperature + 156752.77) / absolute_pressure)) * \
                   (math.sqrt(math.fabs(pressure[i])))
        velocity_list.append(velocity)
    velocity_avg = sum(velocity_list)/len(velocity_list)
    return velocity_avg


def volume_flow_func(velocity_avg, diameter):
    volume_flow = ((math.pi * (diameter/1000) ** 2)/4) * velocity_avg
    return volume_flow


def mass_flow_func(volume_flow, density):
    mass_flow = round(volume_flow * density, 3)
    return mass_flow


def main():
    temperature = None
    ambient_pressure = None
    static_pressure = None
    prandtl_tube_coefficient = None
    diameter = None
    accuracy = None

    while True:
        interface()
        action = action_func()
        if action == 0:
            if temperature and ambient_pressure and static_pressure and prandtl_tube_coefficient and diameter\
                    and accuracy is not None:
                print("Start of calculations!")
                accuracy_coefficient = accuracy_coef_func(accuracy)
                measurement_coordinates = measurement_points_func(accuracy_coefficient, diameter)
                answer = answer_axis_func()
                if answer == 1:
                    pressure = pressure_measurement_func(measurement_coordinates)
                elif answer == 2:
                    print("First axis measurement")
                    pressure_1 = pressure_measurement_func(measurement_coordinates)
                    print("Second axis measurement")
                    pressure_2 = pressure_measurement_func(measurement_coordinates)
                    pressure = pressure_1 + pressure_2
                absolute_pressure = absolute_pressure_func(static_pressure, ambient_pressure)
                velocity = velocity_calculation(temperature, absolute_pressure, prandtl_tube_coefficient, pressure)
                volume_flow = volume_flow_func(velocity, diameter)
                density = density_func(temperature, absolute_pressure)
                mass_flow = mass_flow_func(volume_flow, density)

                while True:
                    interface_result()
                    action_result = action_func()
                    if action_result == 0:
                        break
                    match action_result:
                        case 1:
                            print("Result is: ", round(volume_flow, 3), " m3/s")
                        case 2:
                            print("Result is ", round(volume_flow * 60, 3), " m3/min")
                        case 3:
                            print("Result is ", round(volume_flow * 3600, 3), " m3/h")
                        case 4:
                            print("Result is ", round(mass_flow, 3), " kg/s")
                        case 5:
                            print("Result is ", round(mass_flow * 60, 3), " kg/min")
                        case 6:
                            print("Result is ", round(mass_flow * 3600, 3), " kg/h")
                        case _:
                            print("Wrong action!")
            else:
                print("Input of necessary data has not been completed!")
                continue
            break
        match action:
            case 1:
                if temperature is not None:
                    print("Temperature data already exist")
                    answer = str(input("Do you want to change temperature of measured gas? (y/n): "))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        temperature = temperature_func()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Temperature of measured gas is still ", temperature)
                    else:
                        print("Wrong answer!")
                else:
                    temperature = temperature_func()
            case 2:
                if ambient_pressure is not None:
                    print("Ambient pressure data already exist")
                    answer = str(input("Do you want to change ambient pressure? (y/n):"))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        ambient_pressure = ambient_pressure_func()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Ambient pressure is still ", ambient_pressure)
                    else:
                        print("Wrong answer!")
                else:
                    ambient_pressure = ambient_pressure_func()
            case 3:
                if static_pressure is not None:
                    print("Static pressure data already exist")
                    answer = str(input("Do you want to change static pressure inside the duct? (y/n):"))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        static_pressure = static_pressure_func()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Static pressure inside the duct is still ", static_pressure)
                    else:
                        print("Wrong answer!")
                else:
                    static_pressure = static_pressure_func()
            case 4:
                if prandtl_tube_coefficient is not None:
                    print("Prandtl tube coefficient data already exist")
                    answer = str(input("Do you want to change Prandtl tube coefficient? (y/n):"))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        prandtl_tube_coefficient = prandtl_coef_func()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Prandtl tube coefficient is still ", prandtl_tube_coefficient)
                    else:
                        print("Wrong answer!")
                else:
                    prandtl_tube_coefficient = prandtl_coef_func()
            case 5:
                if diameter is not None:
                    print("Diameter data already exist")
                    answer = str(input("Do you want to change diameter of the duct? (y/n):"))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        diameter = duct_diameter_func()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Diameter of the duct is still ", diameter)
                    else:
                        print("Wrong answer!")
                else:
                    diameter = duct_diameter_func()
            case 6:
                if accuracy is not None:
                    print("Measurement accuracy data already exist")
                    answer = str(input("Do you want to change accuracy of measurement? (y/n):"))
                    if answer in ["y", "Y", "yes", "Yes", "YES"]:
                        accuracy = measurement_accuracy()
                    elif answer in ["n", "N", "No", "NO"]:
                        print("No change. Accuracy of measurement is still ", accuracy)
                    else:
                        print("Wrong answer!")
                else:
                    accuracy = measurement_accuracy()
            case _:
                print("Wrong action")


main()

print("\n\nPress enter to finish")

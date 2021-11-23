from data_structures import Plane, Flight, Correspondence

entry_filename = "data/instance_L.in"

def getActualPlaneAndFlight(list_planes, list_corr, planes_done):
    actual_plane = None
    actual_flight = None

    for corr in list_corr:
        if (corr.used==False) and (corr.dropped==False):
            actual_flight = corr.origin
            minimum_cost_plane_index = corr.origin.getMinimumPlaneCost(planes_done)
            actual_plane = list_planes[minimum_cost_plane_index]
            break
    return actual_plane, actual_flight
    

def getMinimumDestination(actual_plane, actual_flight, list_corr):
    minimum = {"object": None, "value": float('inf')}
    for flight in list(actual_flight.destinations):
        corres = None
        for corr in list_corr:
            if corr.origin.id==actual_flight.id and corr.destination.id==flight.id:
                corres = corr
                break
        if (flight.costs_list[actual_plane.id - 1] < minimum["value"]) and (corres.used==False) and (corres.dropped==False):
            minimum["object"] = flight
            minimum["value"] = flight.costs_list[actual_plane.id - 1]
    return minimum["object"]

def main(filename):
    file_reader = open(filename, 'r')

    file_content = file_reader.readlines()

    file_reader.close()

    lines = [line.split() for line in file_content]

    line_parameter = lines.pop(0)

    parameters = {
        "Number of flights": int(line_parameter[1]),
        "Number of correspondences": int(line_parameter[3]),
        "Number of planes": int(line_parameter[5]),
        "Non made flight cost": int(line_parameter[7]),
        "Frequency to return": int(line_parameter[9]),
        "Non maintenance cost": int(line_parameter[11])
    }

    planes_list = [Plane(id) for id in range(1, parameters["Number of planes"]+1)]
    correpondences_list = []
    flights_list = []

    for line in lines:

        if line[0].lower() == 'v':
            flight = Flight(int(line[1]), line[3:])
            flights_list.append(flight)
        else:
            corr_id = int(line[1])
            corr_origin = flights_list[int(line[3]) - 1]
            corr_destination = flights_list[int(line[5]) - 1]
            corr_base = True if line[7]=='1' else False
            corr_duration = int(line[9])
            correspondence = Correspondence(corr_id, corr_origin, corr_destination, corr_base,
                                            corr_duration)
            correpondences_list.append(correspondence)
            corr_origin.addDestination(corr_destination)
    
    """ print(parameters)
    print("Le dernier vol", flights_list[:5])
    print("La dernière correspondance", correpondences_list[:5]) """

    actual_plane = None
    actual_flight = None
    planes_done = [False] * len(planes_list)
    planes_number_done = 0

    while len(planes_list)!=planes_number_done:

        if actual_plane==None:
            for index, corr in enumerate(correpondences_list):
                if (corr.used==False) and (corr.dropped==False):
                    actual_flight = corr.origin
                    minimum_cost_plane_index = corr.origin.getMinimumPlaneCost(planes_done)
                    actual_plane = planes_list[minimum_cost_plane_index]
                    actual_plane.populateRotation(actual_flight)
                    correpondences_list[index] = corr
                    break                    
        
        minimum_destination = getMinimumDestination(actual_plane, actual_flight, correpondences_list)
        if minimum_destination==None:
            break
        actual_plane.populateRotation(minimum_destination)
        for index, corr in enumerate(correpondences_list):
            print("Values to see Before",corr, minimum_destination)
            if corr.origin.id == actual_flight.id and corr.destination.id==minimum_destination.id:
                corr.makeCorrespondence(actual_plane)
                correpondences_list[index] = corr
            elif corr.origin.id == actual_flight.id or corr.destination.id==minimum_destination.id:
                corr.dropCorrespondence()
                correpondences_list[index] = corr
            print("Values to see After",corr, minimum_destination)
            
            
        
        actual_flight = minimum_destination
        # print("Plane number ", actual_plane.id, " and flight number ", actual_flight.id)

        if actual_flight.getNumberOfDestinations()==0:
            actual_plane.done = True
            planes_done[actual_plane.id - 1] = True
            planes_number_done += 1
            actual_plane = None
                


    for plane in planes_list:
        print("Number of flights", plane.getNumberOfFlights())
        plane.getFlights()
    print("Total number of flights", parameters["Number of flights"])

main(entry_filename)
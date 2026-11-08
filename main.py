import json
from pathlib import Path
from pprint import pprint

from station import Station
from line import Line
from branch import Branch
from prediction import Prediction
from network import Network

def main() -> None:
    tube = Network()

    # Using pathlib for modern, Pythonic path handling
    base_dir = Path('/modules/cs940/cw1')
    lines_dir = base_dir / 'lines'

    # Populate all the stations and lines to our network
    lines = [
        'bakerloo', 'central', 'circle', 'district', 'hammersmith-city', 
        'jubilee', 'metropolitan', 'northern', 'piccadilly', 'victoria', 'waterloo-city'
    ]

    for line_name in lines:
        file_path = lines_dir / f'{line_name}.json'

        # Explicitly declare utf-8 encoding for safe text parsing
        with file_path.open(mode='r', encoding='utf-8') as f:
            obj = json.load(f)

        line_obj = Line(obj['lineId'], obj['lineName'])

        for stop_point_sequence in obj['stopPointSequences']:
            branch = Branch(
                branch_id=stop_point_sequence['branchId'], 
                next_branch_ids=stop_point_sequence['nextBranchIds']
            )

            for stop_point in stop_point_sequence['stopPoint']:
                station = Station(
                    stop_point['id'], 
                    stop_point['name'], 
                    stop_point['lines'], 
                    stop_point['zone'], 
                    stop_point['lat'], 
                    stop_point['lon']
                )
                branch.add_station(station.station_id)
                tube.add_station(station)

            line_obj.add_branch(branch)

        tube.add_line(line_obj)

    # Populate predictions using the personalized DCS arrivals file[cite: 1]
    arrivals_file = base_dir / 'arrivals' / 'arrivals-5843561.json'
    
    with arrivals_file.open(mode='r', encoding='utf-8') as f:
        arrivals_data = json.load(f)

    for arrival in arrivals_data:
        pred = Prediction(
            arrival['vehicleId'],
            arrival['naptanId'],
            arrival['lineId'],
            arrival['platformName'],
            arrival.get('destinationNaptanId', ''),
            arrival['timeToStation'],
            arrival['currentLocation']
        )
        tube.add_prediction(pred)

    # Preliminary tests
    print('----- Next 6 trains arriving at TCR overall ----')
    pprint(tube.next_arrivals_by_station('940GZZLUTCR', k=6))

    print('\n---- Next 12 trains on the Victoria line ---- ')
    pprint(tube.next_arrivals_by_line('victoria', k=12))

    print('\n---- Next 8 trains at Green park on piccadilly line ---- ')
    pprint(tube.next_arrivals_by_station_and_line(station_id='940GZZLUGPK', line_id='piccadilly', k=8))

    print('\n---- Where is train 012 on the District line going next? (in order) ---- ')
    # If the console returns an empty list for this specific query, open your arrivals-5843561.json 
    # file, find a vehicleId that actually exists on the district line, and replace '012' below.
    pprint(tube.next_stations_by_train(vehicle_id='012', line_id='district', k=10))

if __name__ == '__main__':
    main()
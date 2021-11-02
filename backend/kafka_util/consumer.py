# consumer
from kafka import KafkaConsumer
import json
from datetime import datetime as dt

import threading

#from backend.kafka_util.producer import produce
from kafka_util.producer import produce

#from backend.kafka_util import producer
from kafka_util import producer
# consumer = KafkaConsumer('data', bootstrap_servers=['localhost:9092'],value_deserializer=lambda m: json.loads(m.decode('utf-8')))


# print(consumer)
# for message in consumer:
# print("\n hello")
# print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))

def consumer(plot, b, c, state):
    # dates are as strings in api
    start_date = dt.strptime(b, "%Y-%m-%d")
    end_date = dt.strptime(c, "%Y-%m-%d")

    if plot == 'hist':

        _consumer = KafkaConsumer('state_level', bootstrap_servers=['localhost:9092'],
                                  value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        risk_list = [0, 0, 0, 0]
        thread = threading.Thread(
            target=produce,
            args=(state,),
        )
        thread.start()
        for message in _consumer:
            for day in message.value["riskLevelsTimeseries"]:
                curr_date = dt.strptime(day["date"], "%Y-%m-%d")
                if curr_date > start_date and curr_date < end_date:
                    index = day["overall"]
                    if 0 <= index <= 4:
                        risk_list[index - 1] = risk_list[index - 1] + 1
            break

        output = {'1': risk_list[0], '2': risk_list[1], '3': risk_list[2], '4': risk_list[3]}
        return output





    elif plot == 'pie_chart':
        _consumer = KafkaConsumer('state_level', bootstrap_servers=['localhost:9092'],
                                  value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        thread = threading.Thread(
            target=produce,
            args=(state,),
        )
        thread.start()
        for message in _consumer:
            for day in message.value["actualsTimeseries"]:
                if b == day["date"]:
                    start_dose1 = day["vaccinationsInitiated"] if day["vaccinationsInitiated"] else 0
                    start_dose2 = day["vaccinationsCompleted"] if day["vaccinationsCompleted"] else 0
                if c == day["date"]:
                    end_dose1 = day["vaccinationsInitiated"] if day["vaccinationsInitiated"] else 0
                    end_dose2 = day["vaccinationsCompleted"] if day["vaccinationsCompleted"] else 0

            dose1_perc = ((end_dose1 - start_dose1) / ((end_dose1 - start_dose1) + (end_dose2 - start_dose2))) * 100
            dose2_perc = ((end_dose2 - start_dose2) / ((end_dose1 - start_dose1) + (end_dose2 - start_dose2))) * 100

            output = {'dose1': dose1_perc, 'dose2': dose2_perc}
            print(output)
            return output





    elif plot == 'line':
        _consumer = KafkaConsumer('state_level', bootstrap_servers=['localhost:9092'],
                                  value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        cases_per_day = {}

        thread = threading.Thread(
            target=produce,
            args=(state,),
        )
        thread.start()
        for message in _consumer:
            for day in message.value["actualsTimeseries"]:
                curr_date = dt.strptime(day["date"], "%Y-%m-%d")
                if curr_date >= start_date and curr_date <= end_date:
                    cases_per_day[day["date"]] = day["cases"]
            break
        return cases_per_day


if __name__ == '__main__':
    # result = {}
    print(consumer('line', '2021-05-01', '2021-9-05', 'NJ'))
    # thread_1 = threading.Thread(
    #     target=consumer,
    #     args=('hist', '2021-05-01', '2021-9-05', 'NJ', result)
    # )
    # thread_1.start()
    # print(result['result'])

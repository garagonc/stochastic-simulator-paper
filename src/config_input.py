input={
    "ESS": {
	"SoC_Value": 50,
        "meta": {
            "ESS_Capacity": 2430,
            "ESS_Max_Charge_Power": 0.62,
            "ESS_Max_Discharge_Power": 0.62,
            "ESS_Max_SoC": 1,
            "ESS_Min_SoC": 0.2
        }
    },
    "PROFEV": {
    	"Start_Time": 7,
	"VAC_SoC_Value": 40,
        "CarPark": {
            "Cars": {
                "Car1": {
                    "Battery_Capacity_kWh": 18.7
                },
                "Car2": {
                    "Battery_Capacity_kWh": 18.7
                },
                "Car3": {
                    "Battery_Capacity_kWh": 18.7
                },
                "Car4": {
                    "Battery_Capacity_kWh": 18.7
                },
                "Car5": {
                    "Battery_Capacity_kWh": 18.7
                }
            },
            "Charging_Station": {
                "Charger1": {
                    "Max_Charging_Power_kW": 7,
                    "Hosted_Car": "Car1",
                    "SoC": 0.5
                },
                "Charger2": {
                    "Max_Charging_Power_kW": 7,
                    "Hosted_Car": "Car2",
                    "SoC": 0.4
                },
                "Charger3": {
                    "Max_Charging_Power_kW": 7,
                    "Hosted_Car": "Car3",
                    "SoC": 0.4
                },
                "Charger4": {
                    "Max_Charging_Power_kW": 22,
                    "Hosted_Car": "Car4",
                    "SoC": 0.3
                },
                "Charger5": {
                    "Max_Charging_Power_kW": 22,
                    "Hosted_Car": "Car5",
                    "SoC": 0.4
                }
            }
        },
        "Uncertainty": {
            "Plugged_Time": {
                "mean": 18.76,
                "std": 1.3
            },
            "Unplugged_Time": {
                "mean": 7.32,
                "std": 0.78
            },
            "simulation_repetition": 10000,
            "ESS_States": {
                "Min": 0,
                "Max": 100,
                "Steps": 10
            },
            "VAC_States": {
                "Min": 0,
                "Max": 100,
                "Steps": 2.5
            }
        },
        "Unit_Consumption_Assumption": 2.5,
        "Unit_Drop_Penalty": 1
    },
    "grid": {
        "meta": {
            "Max_Voltage_Drop": 1.2315135,
            "Min_Voltage_Drop": 1.0246457,
            "P_Grid_Max_Export_Power": 10,
            "Q_Grid_Max_Export_Power": 10
        }
    },
    "load": {
        "P_Load": [
            -0.057,
            -0.0906,
            -0.0906,
            -0.070066667,
            -0.077533333,
            -0.0906,
            -0.0906,
            -0.10935,
            -0.38135,
            -1.473716667,
            -0.988183333,
            -2.4413,
            -0.4216,
            -0.21725,
            -0.4536,
            -0.4899,
            -0.092466667,
            -0.088733333,
            -0.0906,
            -0.47475,
            -0.48255,
            -1.051866667,
            -1.296316667,
            -0.200733333,
            -0.057,
            -0.0906,
            -0.0906,
            -0.070066667,
            -0.077533333,
            -0.0906,
            -0.0906,
            -0.10935,
            -0.38135,
            -1.473716667,
            -0.988183333,
            -2.4413,
            -0.4216,
            -0.21725,
            -0.4536,
            -0.4899,
            -0.092466667,
            -0.088733333,
            -0.0906,
            -0.47475,
            -0.48255,
            -1.051866667,
            -1.296316667,
            -0.200733333
        ],
        "Q_Load": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "meta": {
            "pf_Load": 1
        }
    },
    "photovoltaic": {
        "P_PV": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0.2264970239999999,
            0.6033471231999998,
            0.9647959893000002,
            1.26597232779,
            1.413326208000001,
            1.485485568000001,
            1.484035606999999,
            1.41545815672,
            1.198723968000001,
            0.8072546816799984,
            0.2925237658,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0.2264970239999999,
            0.6033471231999998,
            0.9647959893000002,
            1.26597232779,
            1.413326208000001,
            1.485485568000001,
            1.484035606999999,
            1.41545815672,
            1.198723968000001,
            0.8072546816799984,
            0.2925237658,
            0,
            0,
            0,
            0,
            0
        ],
        "meta": {
            "PV_Inv_Max_Power": 3500
        }
    }
}

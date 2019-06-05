{
    "ESS": {
	"SoC_Value": 40,
        "meta": {
            "ESS_Capacity": 252000,
            "ESS_Max_Charge_Power": 33,
            "ESS_Max_Discharge_Power": 33,
            "ESS_Max_SoC": 1,
            "ESS_Min_SoC": 0.2
        }
    },
    "PROFEV": {
    	"Start_Time": 0,
	"VAC_SoC_Value": 20,
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
                    "SoC": 0.2
                },
                "Charger2": {
                    "Max_Charging_Power_kW": 7,
                    "Hosted_Car": "Car2",
                    "SoC": 0.2
                },
                "Charger3": {
                    "Max_Charging_Power_kW": 7,
                    "Hosted_Car": "Car3",
                    "SoC": 0.2
                },
                "Charger4": {
                    "Max_Charging_Power_kW": 22,
                    "Hosted_Car": "Car4",
                    "SoC": 0.2
                },
                "Charger5": {
                    "Max_Charging_Power_kW": 22,
                    "Hosted_Car": "Car5",
                    "SoC": 0.2
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
                "Min": 20,
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
            "Max_Voltage_Drop": 1.1,
            "Min_Voltage_Drop": 0.90,
            "P_Grid_Max_Export_Power": 1000,
            "Q_Grid_Max_Export_Power": 1000
        }
    },
    "load": {
        "P_Load": [
            -0.57,
            -0.906,
            -0.906,
            -0.70066667,
            -0.77533333,
            -0.906,
            -0.906,
            -1.0935,
            -3.8135,
            -14.73716667,
            -9.88183333,
            -24.413,
            -4.216,
            -2.1725,
            -4.536,
            -4.899,
            -0.92466667,
            -0.88733333,
            -0.906,
            -4.7475,
            -4.8255,
            -10.51866667,
            -12.96316667,
            -2.00733333,
            -0.57,
            -0.906,
            -0.906,
            -0.70066667,
            -0.77533333,
            -0.906,
            -0.906,
            -1.0935,
            -3.8135,
            -14.73716667,
            -9.88183333,
            -24.413,
            -4.216,
            -2.1725,
            -4.536,
            -4.899,
            -0.92466667,
            -0.88733333,
            -0.906,
            -4.7475,
            -4.8255,
            -10.51866667,
            -12.96316667,
            -2.00733333
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
            0.39367,
            4.75361,
            15.1473,
            15.867,
            31.79674,
            38.73189,
            33.29914,
            14.63464,
            24.09385,
            10.87046,
            20.06198,
            10.99505,
            2.28806,
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
            0.44908,
            5.68837,
            8.98529,
            26.33816,
            15.66616,
            28.97914,
            41.16202,
            8.14226,
            10.0315,
            8.41445,
            15.84856,
            2.32287,
            1.95342,
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "meta": {
            "PV_Inv_Max_Power": 3.5
        }
    }
}

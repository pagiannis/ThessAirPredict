import ForecastChart from "../components/ForecastChart";

const Forecast = () => {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-muted-foreground">
          AI-driven predictions for the next 7 days based on local sensor data.
        </p>
      </div>

      <div className="bg-card p-6 rounded-xl border border-border">
        <ForecastChart />
      </div>
    </div>
  );
};

export default Forecast;

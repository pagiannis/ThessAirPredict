import ForecastChart from "../components/ForecastChart";

const Forecast = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Air Quality Forecast
        </h1>
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

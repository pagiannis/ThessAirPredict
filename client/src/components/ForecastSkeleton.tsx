import { Skeleton } from "@/components/ui/skeleton";

const ForecastSkeleton = () => (
  <div className="bg-card p-6 rounded-xl border border-border flex flex-col gap-4">
    <Skeleton className="h-4 w-36" />
    <Skeleton className="h-3 w-52" />
    <div className="flex items-end gap-1 h-48 pt-4">
      {Array.from({ length: 16 }).map((_, i) => (
        <Skeleton
          key={i}
          className="flex-1 rounded-sm"
          style={{ height: `${35 + Math.sin(i * 0.7) * 25 + 20}%` }}
        />
      ))}
    </div>
    <div className="flex justify-between">
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-3 w-10" />
      ))}
    </div>
  </div>
);

export default ForecastSkeleton;

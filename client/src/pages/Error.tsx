import { Link } from "react-router-dom";
import { AlertCircle } from "lucide-react";

const Error = () => {
  return (
    <div className="h-screen flex flex-col items-center justify-center space-y-4 text-center">
      <AlertCircle className="w-12 h-12 text-destructive" />
      <h1 className="text-4xl font-bold">404 - Page Not Found</h1>
      <p className="text-muted-foreground">
        The atmosphere is a bit thin here. We couldn't find what you were
        looking for.
      </p>
      <Link
        to="/"
        className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
      >
        Back to Dashboard
      </Link>
    </div>
  );
};

export default Error;

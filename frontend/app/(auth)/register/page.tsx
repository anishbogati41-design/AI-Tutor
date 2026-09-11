"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AuthCard } from "@/components/auth-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { User } from "@/types/user";

const schema = z
  .object({
    name: z.string().trim().min(1, "Enter your name").max(100),
    email: z.email("Enter a valid email address"),
    password: z.string().min(8, "Use at least 8 characters").max(128),
    confirmPassword: z.string(),
  })
  .refine((values) => values.password === values.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

type RegisterValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterValues>({ resolver: zodResolver(schema) });

  const registration = useMutation({
    mutationFn: ({ confirmPassword: _confirmation, ...values }: RegisterValues) =>
      apiRequest<User>("/auth/register", {
        method: "POST",
        body: JSON.stringify(values),
      }),
    onSuccess: () => router.replace("/login"),
  });

  return (
    <AuthCard
      title="Create your account"
      description="Start with a student account. Administrator access is assigned separately."
      alternateHref="/login"
      alternateLabel="Already registered? Sign in"
    >
      <form
        className="space-y-4"
        onSubmit={handleSubmit((values) => registration.mutate(values))}
      >
        <div>
          <label htmlFor="name" className="mb-2 block text-sm font-semibold">
            Name
          </label>
          <Input id="name" autoComplete="name" {...register("name")} />
          {errors.name && (
            <p className="mt-1 text-sm text-red-700">{errors.name.message}</p>
          )}
        </div>
        <div>
          <label htmlFor="email" className="mb-2 block text-sm font-semibold">
            Email
          </label>
          <Input id="email" type="email" autoComplete="email" {...register("email")} />
          {errors.email && (
            <p className="mt-1 text-sm text-red-700">{errors.email.message}</p>
          )}
        </div>
        <div>
          <label htmlFor="password" className="mb-2 block text-sm font-semibold">
            Password
          </label>
          <Input
            id="password"
            type="password"
            autoComplete="new-password"
            {...register("password")}
          />
          {errors.password && (
            <p className="mt-1 text-sm text-red-700">
              {errors.password.message}
            </p>
          )}
        </div>
        <div>
          <label
            htmlFor="confirmPassword"
            className="mb-2 block text-sm font-semibold"
          >
            Confirm password
          </label>
          <Input
            id="confirmPassword"
            type="password"
            autoComplete="new-password"
            {...register("confirmPassword")}
          />
          {errors.confirmPassword && (
            <p className="mt-1 text-sm text-red-700">
              {errors.confirmPassword.message}
            </p>
          )}
        </div>
        {registration.error && (
          <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
            {registration.error instanceof ApiError
              ? registration.error.message
              : "Unable to create the account"}
          </p>
        )}
        <Button
          type="submit"
          className="w-full"
          disabled={registration.isPending}
        >
          {registration.isPending ? "Creating account…" : "Create account"}
        </Button>
      </form>
    </AuthCard>
  );
}

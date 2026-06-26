from dataclasses import dataclass

from app.config import settings


@dataclass
class PaiementResult:
    success: bool
    reference: str | None = None
    message: str = ""


class PaiementService:

    @staticmethod
    async def traiter_paiement(montant: float, methode: str, devise: str = "EUR") -> PaiementResult:
        if not settings.stripe_api_key:
            return PaiementResult(success=True, reference="SIMULATED-REF", message="Mode simulation")

        try:
            import stripe
            stripe.api_key = settings.stripe_api_key

            payment_intent = stripe.PaymentIntent.create(
                amount=int(montant * 100),
                currency=devise.lower(),
                payment_method_types=[_stripe_method(methode)],
            )
            return PaiementResult(
                success=True,
                reference=payment_intent.id,
                message="Paiement initié",
            )
        except Exception as e:
            return PaiementResult(success=False, message=str(e))

    @staticmethod
    async def confirmer_transaction(payment_intent_id: str) -> PaiementResult:
        if not settings.stripe_api_key:
            return PaiementResult(success=True, reference=payment_intent_id, message="Confirmé (simulation)")

        try:
            import stripe
            stripe.api_key = settings.stripe_api_key
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return PaiementResult(
                success=intent.status == "succeeded",
                reference=intent.id,
                message=f"Statut: {intent.status}",
            )
        except Exception as e:
            return PaiementResult(success=False, message=str(e))

    @staticmethod
    async def rembourser(payment_intent_id: str) -> PaiementResult:
        if not settings.stripe_api_key:
            return PaiementResult(success=True, reference=payment_intent_id, message="Remboursé (simulation)")

        try:
            import stripe
            stripe.api_key = settings.stripe_api_key
            refund = stripe.Refund.create(payment_intent=payment_intent_id)
            return PaiementResult(
                success=refund.status == "succeeded",
                reference=refund.id,
                message=f"Remboursement: {refund.status}",
            )
        except Exception as e:
            return PaiementResult(success=False, message=str(e))


def _stripe_method(methode: str) -> str:
    mapping = {"carte": "card", "paypal": "paypal", "virement": "sepa_debit"}
    return mapping.get(methode, "card")

type CatFactProps = {
  fact: string;
  date?: string;
};

export default function CatFact({ fact }: CatFactProps) {
  return (
    <article>
      <p className="cat-fact">{fact}</p>
    </article>
  );
}
